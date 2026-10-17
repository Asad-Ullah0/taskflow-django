from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


def _style(form, placeholders):
    for name, field in form.fields.items():
        field.widget.attrs.update(
            {"class": "input", "placeholder": placeholders.get(name, field.label)}
        )
        field.help_text = ""
    return form


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = AuthenticationForm(request, data=request.POST or None)
    _style(form, {"username": "Username", "password": "Password"})
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        nxt = request.GET.get("next", "")
        if not url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
            nxt = "dashboard"
        return redirect(nxt)
    return render(request, "auth.html", {"form": form, "mode": "login"})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    _style(
        form,
        {
            "username": "Choose a username",
            "email": "Email (optional)",
            "password1": "Password",
            "password2": "Confirm password",
        },
    )
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        return redirect("dashboard")
    return render(request, "auth.html", {"form": form, "mode": "register"})
