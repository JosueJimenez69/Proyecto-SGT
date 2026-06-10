# Importamos el administrador de Django.
from django.contrib import admin

# Importamos los modelos de la app boards.
from .models import Board, TaskList, Card


# Registramos el modelo Board en el panel admin.
admin.site.register(Board)

# Registramos el modelo TaskList en el panel admin.
admin.site.register(TaskList)

# Registramos el modelo Card en el panel admin.
admin.site.register(Card)