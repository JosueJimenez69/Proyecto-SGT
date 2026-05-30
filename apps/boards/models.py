# Importamos el modelo User nativo de Django para manejar usuarios.
from django.contrib.auth.models import User

# Importamos models para crear las tablas de la base de datos.
from django.db import models


# Modelo que representa un tablero de trabajo.
class Board(models.Model):
    # Título del tablero.
    title = models.CharField(max_length=100)

    # Descripción opcional del tablero.
    description = models.TextField(blank=True, null=True)

    # Usuario propietario del tablero.
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')

    # Usuarios miembros que pueden participar en el tablero.
    members = models.ManyToManyField(User, related_name='boards', blank=True)

    # Fecha de creación automática.
    created_at = models.DateTimeField(auto_now_add=True)

    # Representación del objeto en el panel admin.
    def __str__(self):
        return self.title


# Modelo que representa una lista dentro de un tablero.
class TaskList(models.Model):
    # Tablero al que pertenece la lista.
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')

    # Nombre de la lista.
    title = models.CharField(max_length=100)

    # Posición para ordenar las listas.
    position = models.PositiveIntegerField(default=0)

    # Ordenamiento por posición.
    class Meta:
        ordering = ['position']

    # Representación del objeto.
    def __str__(self):
        return self.title


# Modelo que representa una tarjeta o tarea.
class Card(models.Model):
    # Opciones de estado de la tarjeta.
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('progress', 'En proceso'),
        ('done', 'Finalizada'),
    ]

    # Lista a la que pertenece la tarjeta.
    list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='cards')

    # Título de la tarjeta.
    title = models.CharField(max_length=150)

    # Descripción de la tarea.
    description = models.TextField(blank=True, null=True)

    # Usuario asignado a la tarea.
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_cards')

    # Usuario que creó la tarea.
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_cards')

    # Posición para ordenar tarjetas.
    position = models.PositiveIntegerField(default=0)

    # Estado de la tarea.
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Fecha de creación automática.
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización automática.
    updated_at = models.DateTimeField(auto_now=True)

    # Ordenamiento por posición.
    class Meta:
        ordering = ['position']

    # Representación del objeto.
    def __str__(self):
        return self.title