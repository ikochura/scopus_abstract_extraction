from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from transactions.models import Category, Dataset


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


@login_required()
def run_script(request):
    if request.GET.get('run_script'):
        print(int(request.GET.get('modal')))
        print('Button clicked')
    return render(request, 'core/script_panel.html', {'text': 'Button clicked'})


@login_required()
def choose_category(request, category_id=None):
    if not request.user.is_authenticated:
        return render(request, "core/home.html", {})
    else:
        context = {
            "category_id": category_id,
        }
        return render(request, "core/script_panel.html", context)
