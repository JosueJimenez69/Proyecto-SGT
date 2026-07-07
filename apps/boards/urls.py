"""
URLs de tableros.
"""

from django.urls import path
from . import views

app_name = "boards"

urlpatterns = [

    # ==========================
    # Dashboard principal
    # ==========================
    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    # ==========================
    # CRUD de Tableros
    # ==========================
    path(
        "tableros/crear/",
        views.board_create,
        name="board_create"
    ),

    path(
        "tableros/<int:board_id>/",
        views.board_detail,
        name="board_detail"
    ),

    path(
        "tableros/<int:board_id>/editar/",
        views.board_update,
        name="board_update"
    ),

    path(
        "tableros/<int:board_id>/eliminar/",
        views.board_delete,
        name="board_delete"
    ),

    # ==========================
    # CRUD de Listas
    # ==========================
    path(
        "tableros/<int:board_id>/listas/crear/",
        views.list_create,
        name="list_create"
    ),

    path(
        "listas/<int:list_id>/editar/",
        views.list_update,
        name="list_update"
    ),

    path(
        "listas/<int:list_id>/eliminar/",
        views.list_delete,
        name="list_delete"
    ),

    # ==========================
    # CRUD de Tarjetas
    # ==========================
    path(
        "listas/<int:list_id>/tarjetas/crear/",
        views.card_create,
        name="card_create"
    ),

    path(
        "tarjetas/<int:card_id>/editar/",
        views.card_update,
        name="card_update"
    ),

    path(
        "tarjetas/<int:card_id>/eliminar/",
        views.card_delete,
        name="card_delete"
    ),

    # ==========================
    # Drag & Drop
    # ==========================
    path(
        "listas/reordenar/",
        views.reorder_lists,
        name="reorder_lists"
    ),

    path(
        "tarjetas/reordenar/",
        views.reorder_cards,
        name="reorder_cards"
    ),

]