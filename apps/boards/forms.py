from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

# Modelos principales de la aplicación boards.
from .models import Board, Card, TaskList


class BoardForm(forms.ModelForm):
    """
    Formulario para crear y editar tableros.

    Permite excluir al propietario de la lista de miembros
    cuando se recibe el usuario mediante el parámetro ``user``.
    """

    class Meta:
        model = Board

        fields = [
            "title",
            "description",
            "members",
        ]

        labels = {
            "title": "Nombre del tablero",
            "description": "Descripción",
            "members": "Miembros",
        }

        help_texts = {
            "members": (
                "Mantén presionada la tecla Ctrl para seleccionar "
                "varios miembros."
            ),
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej.: Proyecto final",
                    "autocomplete": "off",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Describe brevemente el tablero",
                }
            ),
            "members": forms.SelectMultiple(
                attrs={
                    "class": "form-select",
                    "size": 6,
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        """
        Configura dinámicamente los miembros disponibles.

        Si se recibe ``user``, dicho usuario se excluye para evitar
        que el propietario sea agregado también como miembro.
        """

        super().__init__(*args, **kwargs)

        queryset = User.objects.filter(
            is_active=True
        ).order_by("username")

        if user is not None:
            queryset = queryset.exclude(id=user.id)

        self.fields["members"].queryset = queryset

    def clean_members(self):
        """
        Evita guardar al propietario como miembro del mismo tablero.
        """

        members = self.cleaned_data.get("members")

        if (
            self.instance
            and self.instance.pk
            and self.instance.owner_id
        ):
            members = members.exclude(
                id=self.instance.owner_id
            )

        return members


class TaskListForm(forms.ModelForm):
    """
    Formulario para crear y editar listas.

    La posición no se muestra porque se administra automáticamente
    mediante Drag & Drop.
    """

    class Meta:
        model = TaskList

        fields = [
            "title",
        ]

        labels = {
            "title": "Nombre de la lista",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej.: Pendientes",
                    "autocomplete": "off",
                }
            ),
        }


class CardForm(forms.ModelForm):
    """
    Formulario para crear y editar tarjetas.

    La posición se administra automáticamente mediante Drag & Drop.
    Cuando se recibe un tablero o una lista, solo permite asignar
    usuarios que participan en dicho tablero.
    """

    class Meta:
        model = Card

        fields = [
            "title",
            "description",
            "assigned_to",
            "completed",
        ]

        labels = {
            "title": "Título de la tarjeta",
            "description": "Descripción",
            "assigned_to": "Asignar a",
            "completed": "Marcar como finalizada",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej.: Preparar documentación",
                    "autocomplete": "off",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Describe la tarea",
                }
            ),
            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "completed": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def __init__(
        self,
        *args,
        board=None,
        task_list=None,
        **kwargs,
    ):
        """
        Filtra los usuarios asignables.

        Si se recibe ``task_list``, se obtiene el tablero desde ella.
        Si no se recibe contexto, se muestran usuarios activos para
        mantener compatibilidad con las vistas existentes.
        """

        super().__init__(*args, **kwargs)

        if task_list is not None:
            board = task_list.board

        if board is not None:
            queryset = User.objects.filter(
                Q(id=board.owner_id)
                | Q(boards=board)
            ).distinct().order_by("username")
        else:
            queryset = User.objects.filter(
                is_active=True
            ).order_by("username")

        self.fields["assigned_to"].queryset = queryset
        self.fields["assigned_to"].empty_label = "Sin asignar"