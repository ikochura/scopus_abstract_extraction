from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import CategoryForm


@login_required()
def category_view(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        category = form.save(commit=False)
        category.user = request.user
        category = form.save()
        # adds users deposit to balance.
        messages.success(request, 'You create category {} $.'
                         .format(category.name_group_dataset))
        return redirect("home")

    context = {
        "title": "Category",
        "form": form
    }
    return render(request, "transactions/form.html", context)

# @login_required()
# def withdrawal_view(request):
#     form = WithdrawalForm(request.POST or None, user=request.user)
#
#     if form.is_valid():
#         withdrawal = form.save(commit=False)
#         withdrawal.user = request.user
#         withdrawal.save()
#         # subtracts users withdrawal from balance.
#         withdrawal.user.account.save()
#
#         messages.success(
#             request, 'You Have Withdrawn {} $.'.format(withdrawal.amount)
#         )
#         return redirect("home")
#
#     context = {
#         "title": "Withdraw",
#         "form": form
#     }
#     return render(request, "transactions/form.html", context)
