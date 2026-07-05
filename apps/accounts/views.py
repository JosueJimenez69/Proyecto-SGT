"""
Vistas de autenticación.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import RegisterForm


def register_view(request):
    """
    Permite registrar un nuevo usuario en el sistema.
    """

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("boards:dashboard")

    else:
        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form
        }
    )