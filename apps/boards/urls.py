"""
URLs de tableros.
"""

from django.urls import path
from . import views

app_name = "boards"

urlpatterns = [

    # Dashboard principal
    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    # Crear tablero
    path(
        "tableros/crear/",
        views.board_create,
        name="board_create"
    ),

    # Ver detalle del tablero
    path(
        "tableros/<int:board_id>/",
        views.board_detail,
        name="board_detail"
    ),

    # Editar tablero
    path(
        "tableros/<int:board_id>/editar/",
        views.board_update,
        name="board_update"
    ),

    # Eliminar tablero
    path(
        "tableros/<int:board_id>/eliminar/",
        views.board_delete,
        name="board_delete"
    ),

    # Crear lista
    path(
        "tableros/<int:board_id>/listas/crear/",
        views.list_create,
        name="list_create"
    ),

    # Crear tarjeta
    path(
        "listas/<int:list_id>/tarjetas/crear/",
        views.card_create,
        name="card_create"
    ),

]