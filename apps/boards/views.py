from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Board, TaskList, Card
from .forms import BoardForm, TaskListForm, CardForm
# pyrefly: ignore [missing-import]
from apps.notifications.models import Notification


@login_required
def dashboard(request):
    """
    Muestra los tableros donde el usuario es propietario o miembro.
    También muestra las últimas notificaciones no leídas del usuario.
    """
    boards = Board.objects.filter(
        Q(owner=request.user) | Q(members=request.user)
    ).distinct()

    notifications = request.user.notifications.filter(
        is_read=False
    ).order_by("-created_at")[:5]

    return render(request, "boards/dashboard.html", {
        "boards": boards,
        "notifications": notifications
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
def board_update(request, board_id):
    """
    Permite editar un tablero existente.
    """
    board = get_object_or_404(
        Board,
        id=board_id,
        owner=request.user
    )

    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Tablero actualizado correctamente."
            )

            return redirect("boards:dashboard")

    else:
        form = BoardForm(instance=board)

    return render(
        request,
        "boards/board_form.html",
        {
            "form": form,
            "titulo": "Editar tablero"
        }
    )


@login_required
def board_delete(request, board_id):
    """
    Permite eliminar un tablero del usuario.
    """
    board = get_object_or_404(
        Board,
        id=board_id,
        owner=request.user
    )

    if request.method == "POST":
        board.delete()

        messages.success(
            request,
            "Tablero eliminado correctamente."
        )

        return redirect("boards:dashboard")

    return render(
        request,
        "boards/board_delete.html",
        {
            "board": board
        }
    )


@login_required
def list_create(request, board_id):
    """
    Permite crear una nueva lista dentro de un tablero del usuario.
    """
    board = get_object_or_404(
        Board,
        id=board_id,
        owner=request.user
    )

    if request.method == "POST":
        form = TaskListForm(request.POST)

        if form.is_valid():
            task_list = form.save(commit=False)
            task_list.board = board
            task_list.save()

            messages.success(
                request,
                "Lista creada correctamente."
            )

            return redirect(
                "boards:board_detail",
                board_id=board.id
            )

    else:
        form = TaskListForm()

    return render(
        request,
        "boards/list_form.html",
        {
            "form": form,
            "board": board
        }
    )


@login_required
def list_update(request, list_id):
    """
    Permite editar una lista existente.
    """
    task_list = get_object_or_404(
        TaskList,
        id=list_id,
        board__owner=request.user
    )

    if request.method == "POST":
        form = TaskListForm(
            request.POST,
            instance=task_list
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Lista actualizada correctamente."
            )

            return redirect(
                "boards:board_detail",
                board_id=task_list.board.id
            )

    else:
        form = TaskListForm(instance=task_list)

    return render(
        request,
        "boards/list_form.html",
        {
            "form": form,
            "board": task_list.board
        }
    )


@login_required
def list_delete(request, list_id):
    """
    Permite eliminar una lista del tablero.
    """
    task_list = get_object_or_404(
        TaskList,
        id=list_id,
        board__owner=request.user
    )

    board_id = task_list.board.id

    if request.method == "POST":
        task_list.delete()

        messages.success(
            request,
            "Lista eliminada correctamente."
        )

        return redirect(
            "boards:board_detail",
            board_id=board_id
        )

    return render(
        request,
        "boards/list_delete.html",
        {
            "task_list": task_list
        }
    )


@login_required
def card_create(request, list_id):
    """
    Permite crear una nueva tarjeta dentro de una lista.
    Si la tarjeta se asigna a un usuario, genera una notificación.
    """
    task_list = get_object_or_404(
        TaskList,
        id=list_id,
        board__owner=request.user
    )

    if request.method == "POST":
        form = CardForm(request.POST)

        if form.is_valid():
            card = form.save(commit=False)
            card.task_list = task_list
            card.save()

            if card.assigned_to:
                Notification.objects.create(
                    user=card.assigned_to,
                    message=f"Se te asignó la tarjeta: {card.title}"
                )

            messages.success(
                request,
                "Tarjeta creada correctamente."
            )

            return redirect(
                "boards:board_detail",
                board_id=task_list.board.id
            )

    else:
        form = CardForm()

    return render(
        request,
        "boards/card_form.html",
        {
            "form": form,
            "task_list": task_list
        }
    )


@login_required
def card_update(request, card_id):
    """
    Permite editar una tarjeta existente.
    """
    card = get_object_or_404(
        Card,
        id=card_id,
        task_list__board__owner=request.user
    )

    if request.method == "POST":
        form = CardForm(
            request.POST,
            instance=card
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Tarjeta actualizada correctamente."
            )

            return redirect(
                "boards:board_detail",
                board_id=card.task_list.board.id
            )

    else:
        form = CardForm(instance=card)

    return render(
        request,
        "boards/card_form.html",
        {
            "form": form,
            "task_list": card.task_list
        }
    )


@login_required
def card_delete(request, card_id):
    """
    Permite eliminar una tarjeta.
    """
    card = get_object_or_404(
        Card,
        id=card_id,
        task_list__board__owner=request.user
    )

    board_id = card.task_list.board.id

    if request.method == "POST":
        card.delete()

        messages.success(
            request,
            "Tarjeta eliminada correctamente."
        )

        return redirect(
            "boards:board_detail",
            board_id=board_id
        )

    return render(
        request,
        "boards/card_delete.html",
        {
            "card": card
        }
    )