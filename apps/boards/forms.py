from django import forms

# Importamos los modelos principales de la app boards.
from .models import Board, TaskList, Card


class BoardForm(forms.ModelForm):
    """
    Formulario para crear y editar tableros.
    """

    class Meta:
        model = Board

        fields = [
            'title',
            'description',
            'members'
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),
            'members': forms.SelectMultiple(
                attrs={'class': 'form-control'}
            ),
        }


class TaskListForm(forms.ModelForm):
    """
    Formulario para crear listas dentro de un tablero.
    """

    class Meta:
        model = TaskList

        fields = [
            'title',
            'position'
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'position': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
        }


class CardForm(forms.ModelForm):
    """
    Formulario para crear y editar tarjetas o tareas.
    """

    class Meta:
        model = Card

        fields = [
            'title',
            'description',
            'assigned_to',
            'position',
            'completed'
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),
            'assigned_to': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'position': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'completed': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }