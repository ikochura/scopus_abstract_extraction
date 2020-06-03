from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import (
    UserLoginForm, UserRegistrationForm,

)


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        user_form = UserRegistrationForm(
            request.POST or None,
        )

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            new_user = authenticate(email=user.email, password=password)
            login(request, new_user, backend='accounts.backends.AccountNoBackend')
            messages.success(request,
                             '''Thank You For Creating an account {}.
                             Your email is {}, Please use it to login
                             '''.format(new_user.full_name, new_user.email))

            return redirect("home")

        context = {
            "title": "Sign up",
            "user_form": user_form,
        }

        return render(request, "accounts/register_form.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            # authenticate with Account No & Password
            user = authenticate(email=email, password=password)
            login(request, user, backend='accounts.backends.AccountNoBackend')
            messages.success(request, 'Welcome, {}!'.format(user.full_name))
            return redirect("home")

        context = {"form": form,
                   "title": "Sign in",
                   }

        return render(request, "accounts/form.html", context)


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    else:
        logout(request)
        return redirect("home")
