from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    """
    Modelo principal de tablero.
    Cada tablero pertenece a un creador y puede tener varios miembros.
    """

    # Nombre del tablero.
    title = models.CharField(
        max_length=150
    )

    # Descripción opcional del tablero.
    description = models.TextField(
        blank=True
    )

    # Usuario propietario del tablero.
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_boards'
    )

    # Usuarios que participan en el tablero.
    members = models.ManyToManyField(
        User,
        related_name='boards',
        blank=True
    )

    # Fecha de creación automática.
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Fecha de última actualización.
    updated_at = models.DateTimeField(
        auto_now=True
    )

    # Representación en texto del objeto.
    def __str__(self):
        return self.title


class TaskList(models.Model):
    """
    Representa una lista dentro de un tablero.
    Ejemplo: Pendientes, En proceso o Finalizadas.
    """

    # Tablero al que pertenece la lista.
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='lists'
    )

    # Nombre de la lista.
    title = models.CharField(
        max_length=150
    )

    # Posición para ordenar listas en el tablero.
    position = models.PositiveIntegerField(
        default=0
    )

    # Fecha de creación automática.
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["position"]

    # Representación en texto del objeto.
    def __str__(self):
        return self.title


class Card(models.Model):
    """
    Tarjeta o tarea dentro de una lista.
    """

    # Lista a la que pertenece la tarjeta.
    task_list = models.ForeignKey(
        TaskList,
        on_delete=models.CASCADE,
        related_name='cards'
    )

    # Título de la tarea.
    title = models.CharField(
        max_length=200
    )

    # Descripción detallada de la tarea.
    description = models.TextField(
        blank=True
    )

    # Usuario asignado a la tarea.
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_cards'
    )

    # Posición para ordenar tarjetas dentro de una lista.
    position = models.PositiveIntegerField(
        default=0
    )

    # Estado de finalización de la tarea.
    completed = models.BooleanField(
        default=False
    )

    # Fecha de creación automática.
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Fecha de última actualización.
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["position"]

    # Representación en texto del objeto.
    def __str__(self):
        return self.title