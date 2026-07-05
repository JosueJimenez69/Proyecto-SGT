"""
URLs de tableros.
"""

from django.urls import path
from . import views

app_name = "boards"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("tableros/crear/", views.board_create, name="board_create"),
    path("tableros/<int:board_id>/", views.board_detail, name="board_detail"),
    path("tableros/<int:board_id>/listas/crear/", views.list_create, name="list_create"),
    path("listas/<int:list_id>/tarjetas/crear/", views.card_create, name="card_create"),
]