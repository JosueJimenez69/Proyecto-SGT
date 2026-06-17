from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    """
    Modelo para guardar notificaciones básicas del sistema.
    Cada notificación pertenece a un usuario.
    """

    # Usuario que recibe la notificación.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    # Mensaje de la notificación.
    message = models.CharField(
        max_length=255
    )

    # Indica si el usuario ya leyó la notificación.
    is_read = models.BooleanField(
        default=False
    )

    # Fecha de creación automática.
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Representación en texto del objeto.
    def __str__(self):
        return f"{self.user.username} - {self.message}"