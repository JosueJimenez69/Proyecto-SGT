from django.contrib import admin

# Importamos el modelo Notification para administrarlo desde Django Admin.


# pyrefly: ignore [missing-import]
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Configuración del panel administrativo para notificaciones.
    """

    # Campos visibles en el listado de notificaciones.
    list_display = (
        'user',
        'message',
        'is_read',
        'created_at'
    )

    # Filtro para ver notificaciones leídas o no leídas.
    list_filter = (
        'is_read',
    )

    # Permite buscar por usuario o mensaje.
    search_fields = (
        'user__username',
        'message'
    )