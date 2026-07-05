from django.contrib import admin

# Importamos los modelos que serán administrados desde Django Admin.
# pyrefly: ignore [missing-import]
from .models import Board, TaskList, Card

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """
    Configuración del panel administrativo para tableros.
    """

    # Campos que se mostrarán en la lista de tableros.
    list_display = (
        'title',
        'owner',
        'created_at'
    )

    # Permite realizar búsquedas por título y propietario.
    search_fields = (
        'title',
        'owner__username'
    )

    # Muestra una interfaz amigable para seleccionar miembros.
    filter_horizontal = (
        'members',
    )


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    """
    Configuración del panel administrativo para listas.
    """

    # Campos visibles en el listado.
    list_display = (
        'title',
        'board',
        'position'
    )

    # Filtro por tablero.
    list_filter = (
        'board',
    )


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    """
    Configuración del panel administrativo para tarjetas.
    """

    # Campos visibles en el listado.
    list_display = (
        'title',
        'task_list',
        'assigned_to',
        'completed'
    )

    # Filtro por estado de la tarjeta.
    list_filter = (
        'completed',
    )

    # Búsqueda por título de la tarjeta.
    search_fields = (
        'title',
    )