from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from transactions.models import Category, Dataset
import psycopg2


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


def run_script(request):
    if request.method == 'POST' and 'run_script' in request.POST:

        # call function
        # getAbstractScript()
        # return user to required page
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "core/home.html", {})


@login_required()
def choose_category(request, category_id=None):
    id = request.GET.get(id(), None)
    response = "You're looking at the results of question %s."
    return HttpResponse(response % id)
