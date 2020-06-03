from datetime import datetime
import logging
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from transactions.models import Category, Dataset, Document

logger = logging.getLogger(__name__)


def home(request):
    if not request.user.is_authenticated:
        return render(request, "core/home.html", {})
    else:
        user = request.user
        category = Category.objects.filter(user=request.user)
        category_obj = Dataset.objects.filter(category__user=request.user)
        context = {
            "user": user,
            "category": category,
            "category_obj": category_obj,
        }

        return render(request, "core/transactions.html", context)


def about(request):
    return render(request, "core/about.html", {})


API_KEY = 'e947957924671f20b87c8437ae30ba05'


def run_scopus_search(query):
    return requests.get(
        'https://api.elsevier.com/content/search/scopus?&query=%s&field=dc:identifier' % query,
        headers={'Accept': 'application/json', 'X-ELS-APIKey': API_KEY}).json()


def get_scopus_ids(res):
    return [[str(r['dc:identifier'])] for r in res['search-results']['entry']]


def get_scopus_info(id):
    url = ('https://api.elsevier.com/content/abstract/scopus_id/' + id + '?field=dc:description')
    return requests.get(url, headers={'Accept': 'application/json', 'X-ELS-APIKey': API_KEY}).json()


@login_required()
def get_abstract(request, category_id=None):
    if Document.objects.filter(category=category_id):
        file_obj = Document.objects.get(category=category_id).docfile
    else:
        return render(request, "transactions/upload_doc.html")
    with file_obj as file:
        for line in file:
            line = str(line)[2:-3]
            results = run_scopus_search(line)
            try:
                scopus_ids = get_scopus_ids(results)[0]
                try:
                    results_info = get_scopus_info(scopus_ids[0])
                    try:
                        abstract = results_info['abstracts-retrieval-response']['coredata']['dc:description']
                        if abstract == 'None':
                            logger.error(scopus_ids[0], " None", end='')
                            continue
                        Dataset(scopus_id=scopus_ids[0], abstract=abstract, timestamp=datetime.now(),
                                category_id=category_id).save()
                    except Exception as e:
                        logger.error(e, "\nAbstract not available")
                        continue
                except Exception as e:
                    logger.error(e, '\n', scopus_ids[0], "Result error")
                    continue
            except Exception as e:
                logger.error(e, 'Error get_scopus_ids')
    if not request.user.is_authenticated:
        return render(request, "core/home.html", {})
    else:
        context = {
            "text": line,
        }
        return render(request, "core/script_panel.html", context)
