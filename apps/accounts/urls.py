"""
URLs de autenticación.
"""

from django.urls import path
from .views import register_view

app_name = "accounts"

urlpatterns = [
    path(
        "registro/",
        register_view,
        name="register"
    ),
]