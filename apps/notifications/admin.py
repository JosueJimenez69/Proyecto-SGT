# Importamos el administrador de Django.
from django.contrib import admin

# Importamos el modelo Notification.
from .models import Notification


# Registramos Notification en el panel admin.
admin.site.register(Notification)