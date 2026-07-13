from django import forms
from django.contrib.auth.models import User

from .models import Board, Card, TaskList


class BoardForm(forms.ModelForm):
    """
    Formulario para crear y editar tableros.

    Permite seleccionar varios miembros y excluye al propietario
    de la lista de usuarios disponibles.
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
        Excluye al usuario actual de la lista de miembros.
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
        Evita que el propietario quede guardado como miembro.
        """

        members = self.cleaned_data.get("members")

        if members is None:
            return members

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

    La posición se administra mediante Drag & Drop.
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

    Solo permite asignar tarjetas a miembros activos del tablero.
    El propietario no aparece como opción.
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
        Determina el tablero y filtra los usuarios asignables.
        """

        super().__init__(*args, **kwargs)

        if task_list is not None:
            board = task_list.board
        elif (
            self.instance
            and self.instance.pk
            and self.instance.task_list_id
        ):
            board = self.instance.task_list.board

        self.board = board

        if board is not None:
            queryset = board.members.filter(
                is_active=True
            ).exclude(
                id=board.owner_id
            ).distinct().order_by("username")
        else:
            queryset = User.objects.none()

        self.fields["assigned_to"].queryset = queryset
        self.fields["assigned_to"].empty_label = "Sin asignar"

    def clean_assigned_to(self):
        """
        Valida que el responsable sea un miembro activo del tablero.
        """

        assigned_to = self.cleaned_data.get("assigned_to")

        if assigned_to is None:
            return None

        if self.board is None:
            raise forms.ValidationError(
                "No se pudo determinar el tablero de la tarjeta."
            )

        if assigned_to.id == self.board.owner_id:
            raise forms.ValidationError(
                "El propietario del tablero no puede ser asignado."
            )

        is_member = self.board.members.filter(
            id=assigned_to.id,
            is_active=True,
        ).exists()

        if not is_member:
            raise forms.ValidationError(
                "La tarjeta solo puede asignarse a un miembro del tablero."
            )

        return assigned_to