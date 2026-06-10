# Importamos el modelo User de Django.
from django.contrib.auth.models import User

# Importamos models para crear la tabla Notification.
from django.db import models


# Modelo que representa una notificación para un usuario.
class Notification(models.Model):
    # Usuario que recibirá la notificación.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    # Mensaje de la notificación.
    message = models.CharField(max_length=255)

    # Indica si la notificación fue leída.
    is_read = models.BooleanField(default=False)

    # Fecha de creación automática.
    created_at = models.DateTimeField(auto_now_add=True)

    # Ordenamos primero las notificaciones más recientes.
    class Meta:
        ordering = ['-created_at']

    # Representación del objeto.
    def __str__(self):
        return self.message