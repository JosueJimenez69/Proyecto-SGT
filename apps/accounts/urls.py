"""
URLs relacionadas con la autenticación.
"""

from django.urls import path
from .views import (
    register_view,
    password_reset_request
)

app_name = "accounts"

urlpatterns = [

    path(
        "registro/",
        register_view,
        name="register"
    ),

    path(
        "recuperar/",
        password_reset_request,
        name="password_reset"
    ),

]