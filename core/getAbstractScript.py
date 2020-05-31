from pathlib import Path
from itertools import islice

import pandas as pd
import requests

from scopus_api_key import API_KEY


def run_scopus_search(query):
    return requests.get(
        'https://api.elsevier.com/content/search/scopus?&query=%s&field=dc:identifier' % query,
        headers={'Accept': 'application/json', 'X-ELS-APIKey': API_KEY}).json()


def get_scopus_ids(res):
    return [[str(r['dc:identifier'])] for r in res['search-results']['entry']]


def get_scopus_info(ID):
    url = ('https://api.elsevier.com/content/abstract/scopus_id/' + ID + '?field=dc:description')
    return requests.get(url, headers={'Accept': 'application/json', 'X-ELS-APIKey': API_KEY}).json()


def skip_line(missing_lines, existing_lines):
    with open('./data/unavailable_articles_count_1.txt', 'w') as file:
        file.write(''.join(str(missing_lines) + ' ' + str(existing_lines)))


base = Path('./data/scopus_search_base_1.csv')
base_exist = False
new_base_exist = False
unavailable_articles_count = 0
number_articles_already_load = 0
if base.is_file():
    with open('./data/unavailable_articles_count_1.txt', 'r') as file:
        file_list = list(map(int, file.read().split()))
    base_exist = True
    number_articles_already_load = int(file_list[1])
    unavailable_articles_count = int(file_list[0])
    print('base exists %d articles ' % number_articles_already_load)
new_base_exist = base_exist

article_data = []
if number_articles_already_load != 0 or unavailable_articles_count != 0:
    start = number_articles_already_load + unavailable_articles_count
else:
    start = 0
n = 0
with open('./data/dois.txt', 'r') as f:
    lines = islice(f, start, None)
    for line in lines:
        results = run_scopus_search(line)
        skip_line(unavailable_articles_count, number_articles_already_load)
        try:
            scopus_ids = get_scopus_ids(results)[0]
            nn = 0
            try:
                results_info = get_scopus_info(scopus_ids[0])
                try:
                    abstract = results_info['abstracts-retrieval-response']['coredata']['dc:description']
                    if abstract == 'None':
                        print(scopus_ids[0], " None", end='')
                        unavailable_articles_count += 1
                        continue
                    number_articles_already_load += 1
                    print(number_articles_already_load)
                    article_data.append(
                        {'Scopus_ID': scopus_ids[0], 'abstract': abstract})
                    n += 1
                    nn += 1
                except Exception as e:
                    # print(e, '\n', s_id[0], "Abstract not available")
                    unavailable_articles_count += 1
                    continue
            except Exception as e:
                print(e, '\n', scopus_ids[0], "Result error")
                unavailable_articles_count += 1
                continue
            if nn > 0:
                article_set = pd.DataFrame(article_data)
                article_data = []
                if not new_base_exist:
                    print('creating base')
                    article_set.to_csv('./data/scopus_search_base_1.csv', index=False)
                    new_base_exist = True
                else:
                    article_set.to_csv('./data/scopus_search_base_1.csv', mode='a', header=False, index=False)
        except Exception as e:
            print(e, 'Error get_scopus_ids')
            unavailable_articles_count += 1
            continue
