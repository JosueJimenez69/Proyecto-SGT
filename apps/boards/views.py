from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Board, TaskList, Card
from .forms import BoardForm, TaskListForm, CardForm


@login_required
def dashboard(request):
    """
    Muestra los tableros donde el usuario es propietario o miembro.
    """
    boards = Board.objects.filter(
        Q(owner=request.user) | Q(members=request.user)
    ).distinct()

    return render(request, "boards/dashboard.html", {
        "boards": boards
    })


@login_required
def board_detail(request, board_id):
    """
    Muestra el detalle de un tablero con sus listas y tarjetas.
    """
    board = get_object_or_404(
        Board,
        Q(id=board_id),
        Q(owner=request.user) | Q(members=request.user)
    )

    lists = board.lists.all().order_by("position")

    return render(request, "boards/board_detail.html", {
        "board": board,
        "lists": lists
    })


@login_required
def board_create(request):
    """
    Permite crear un nuevo tablero y asigna como propietario al usuario actual.
    """
    if request.method == "POST":
        form = BoardForm(request.POST)

        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            form.save_m2m()

            messages.success(request, "Tablero creado correctamente.")
            return redirect("boards:dashboard")
    else:
        form = BoardForm()

    return render(request, "boards/board_form.html", {
        "form": form,
        "titulo": "Crear tablero"
    })


@login_required
def list_create(request, board_id):
    """
    Permite crear una nueva lista dentro de un tablero del usuario.
    """
    board = get_object_or_404(Board, id=board_id, owner=request.user)

    if request.method == "POST":
        form = TaskListForm(request.POST)

        if form.is_valid():
            task_list = form.save(commit=False)
            task_list.board = board
            task_list.save()

            messages.success(request, "Lista creada correctamente.")
            return redirect("boards:board_detail", board_id=board.id)
    else:
        form = TaskListForm()

    return render(request, "boards/list_form.html", {
        "form": form,
        "board": board
    })


@login_required
def card_create(request, list_id):
    """
    Permite crear una nueva tarjeta dentro de una lista.
    """
    task_list = get_object_or_404(TaskList, id=list_id)

    if request.method == "POST":
        form = CardForm(request.POST)

        if form.is_valid():
            card = form.save(commit=False)
            card.task_list = task_list
            card.save()

            messages.success(request, "Tarjeta creada correctamente.")
            return redirect("boards:board_detail", board_id=task_list.board.id)
    else:
        form = CardForm()

    return render(request, "boards/card_form.html", {
        "form": form,
        "task_list": task_list
    })