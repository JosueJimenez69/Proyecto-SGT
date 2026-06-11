from django import forms  # Importamos formularios de Django.

from .models import Board, TaskList, Card  # Importamos los modelos principales.


class BoardForm(forms.ModelForm):
    # Formulario para crear y editar tableros.
    class Meta:
        model = Board  # Modelo asociado.
        fields = ['title', 'description', 'members']  # Campos visibles.
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # Input Bootstrap.
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),  # Área de texto.
            'members': forms.SelectMultiple(attrs={'class': 'form-control'}),  # Selección múltiple.
        }


class TaskListForm(forms.ModelForm):
    # Formulario para crear listas dentro de un tablero.
    class Meta:
        model = TaskList  # Modelo asociado.
        fields = ['title', 'position']  # Campos visibles.
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # Input Bootstrap.
            'position': forms.NumberInput(attrs={'class': 'form-control'}),  # Número de posición.
        }


class CardForm(forms.ModelForm):
    # Formulario para crear tarjetas o tareas.
    class Meta:
        model = Card  # Modelo asociado.
        fields = ['title', 'description', 'assigned_to', 'position', 'status']  # Campos visibles.
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # Título.
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),  # Descripción.
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),  # Usuario asignado.
            'position': forms.NumberInput(attrs={'class': 'form-control'}),  # Posición.
            'status': forms.Select(attrs={'class': 'form-control'}),  # Estado.
        }