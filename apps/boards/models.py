from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    """
    Modelo principal de tablero.
    Cada tablero pertenece a un creador y puede tener varios miembros.
    """

    title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_boards'
    )

    members = models.ManyToManyField(
        User,
        related_name='boards',
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title


class TaskList(models.Model):
    """
    Representa una lista dentro de un tablero.
    """

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='lists'
    )

    title = models.CharField(
        max_length=150
    )

    position = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Card(models.Model):
    """
    Tarjeta o tarea dentro de una lista.
    """

    task_list = models.ForeignKey(
        TaskList,
        on_delete=models.CASCADE,
        related_name='cards'
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_cards'
    )

    position = models.PositiveIntegerField(
        default=0
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title