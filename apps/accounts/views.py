"""
Vistas relacionadas con la autenticación de usuarios.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .forms import RegisterForm


def register_view(request):
    """
    Permite registrar un nuevo usuario en el sistema.
    """

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            # Guarda el nuevo usuario en la base de datos
            user = form.save()

            # Inicia sesión automáticamente
            login(request, user)

            # Mensaje de éxito
            messages.success(
                request,
                "Cuenta creada correctamente. Bienvenido al sistema."
            )

            # Redirecciona al Dashboard
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


def password_reset_request(request):
    """
    Solicita el correo electrónico del usuario para recuperar la contraseña.

    En esta versión del proyecto no se envía un correo real.
    Se muestra un mensaje informativo simulando el proceso.
    """

    if request.method == "POST":

        email = request.POST.get("email")

        messages.success(
            request,
            "Si el correo electrónico se encuentra registrado, recibirás un enlace para restablecer tu contraseña."
        )

        return redirect("login")

    return render(
        request,
        "registration/password_reset.html"
    )