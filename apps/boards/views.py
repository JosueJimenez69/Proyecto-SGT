"""
Vistas principales de la aplicación de tableros.

Este módulo administra:
- Dashboard.
- CRUD de tableros.
- CRUD de listas.
- CRUD de tarjetas.
- Notificaciones.
- Drag & Drop.
- Actualizaciones en tiempo real mediante WebSockets.
"""

import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

# pyrefly: ignore [missing-import]
from apps.notifications.models import Notification

from .forms import BoardForm, CardForm, TaskListForm
from .models import Board, Card, TaskList


def send_board_update(board_id, message):
    """
    Envía una actualización al grupo WebSocket del tablero.

    Todos los usuarios que tengan abierto el mismo tablero
    recibirán el mensaje en tiempo real.
    """

    channel_layer = get_channel_layer()

    if channel_layer is None:
        return

    async_to_sync(channel_layer.group_send)(
        f"board_{board_id}",
        {
            "type": "board_update",
            "message": message,
        },
    )


def notify_board_members(board, message, exclude_user=None):
    """
    Crea una notificación para los miembros de un tablero.

    El usuario indicado en exclude_user no recibirá la notificación.
    """

    recipients = list(board.members.all())

    # También incluye al propietario si no está ya en la lista.
    if board.owner not in recipients:
        recipients.append(board.owner)

    for user in recipients:
        if exclude_user is not None and user == exclude_user:
            continue

        Notification.objects.create(
            user=user,
            message=message,
        )


def is_board_participant(board, user):
    """
    Indica si el usuario es propietario o miembro del tablero.
    """

    return (
        user == board.owner
        or board.members.filter(id=user.id).exists()
    )



@login_required
def dashboard(request):
    """
    Muestra los tableros donde el usuario es propietario o miembro.

    También muestra las últimas cinco notificaciones no leídas.
    """

    boards = Board.objects.filter(
        Q(owner=request.user) | Q(members=request.user)
    ).distinct()

    notifications = request.user.notifications.filter(
        is_read=False
    ).order_by("-created_at")[:5]

    return render(
        request,
        "boards/dashboard.html",
        {
            "boards": boards,
            "notifications": notifications,
        },
    )


@login_required
def board_detail(request, board_id):
    """
    Muestra un tablero con sus listas y tarjetas ordenadas.

    El usuario debe ser propietario o miembro. Se usa distinct()
    para evitar resultados duplicados cuando existen varios miembros.
    """

    accessible_boards = Board.objects.filter(
        Q(owner=request.user) | Q(members=request.user)
    ).distinct()

    board = get_object_or_404(
        accessible_boards,
        id=board_id,
    )

    lists = board.lists.prefetch_related(
        "cards",
        "cards__assigned_to",
    ).order_by("position")

    return render(
        request,
        "boards/board_detail.html",
        {
            "board": board,
            "lists": lists,
        },
    )


@login_required
def board_create(request):
    """
    Crea un tablero y establece al usuario autenticado
    como propietario. El propietario no puede ser miembro.
    """

    if request.method == "POST":
        form = BoardForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            form.save_m2m()

            # Protección adicional: evita guardar al propietario
            # también como miembro del mismo tablero.
            board.members.remove(request.user)

            messages.success(
                request,
                "Tablero creado correctamente.",
            )

            return redirect("boards:dashboard")

    else:
        form = BoardForm(
            user=request.user,
        )

    return render(
        request,
        "boards/board_form.html",
        {
            "form": form,
            "titulo": "Crear tablero",
        },
    )


@login_required
def board_update(request, board_id):
    """
    Edita un tablero.

    Solo el propietario puede realizar esta acción. El propietario
    no aparece entre los miembros seleccionables.
    """

    board = get_object_or_404(
        Board,
        id=board_id,
        owner=request.user,
    )

    if request.method == "POST":
        form = BoardForm(
            request.POST,
            instance=board,
            user=request.user,
        )

        if form.is_valid():
            updated_board = form.save()

            # Protección adicional ante datos manipulados.
            updated_board.members.remove(request.user)

            action_message = (
                f"{request.user.username} actualizó el tablero "
                f"'{updated_board.title}'."
            )

            notify_board_members(
                updated_board,
                action_message,
                exclude_user=request.user,
            )

            send_board_update(
                updated_board.id,
                action_message,
            )

            messages.success(
                request,
                "Tablero actualizado correctamente.",
            )

            return redirect("boards:dashboard")

    else:
        form = BoardForm(
            instance=board,
            user=request.user,
        )

    return render(
        request,
        "boards/board_form.html",
        {
            "form": form,
            "titulo": "Editar tablero",
        },
    )


@login_required
def board_delete(request, board_id):
    """
    Elimina un tablero.

    Solo el propietario puede eliminarlo.
    """

    board = get_object_or_404(
        Board,
        id=board_id,
        owner=request.user,
    )

    if request.method == "POST":
        board_title = board.title

        action_message = (
            f"{request.user.username} eliminó el tablero "
            f"'{board_title}'."
        )

        notify_board_members(
            board,
            action_message,
            exclude_user=request.user,
        )

        send_board_update(
            board.id,
            action_message,
        )

        board.delete()

        messages.success(
            request,
            "Tablero eliminado correctamente.",
        )

        return redirect("boards:dashboard")

    return render(
        request,
        "boards/board_delete.html",
        {
            "board": board,
        },
    )


@login_required
def list_create(request, board_id):
    """
    Crea una lista dentro de un tablero.

    Solo el propietario del tablero puede crearla.
    """

    board = get_object_or_404(
        Board,
        id=board_id,
        owner=request.user,
    )

    if request.method == "POST":
        form = TaskListForm(request.POST)

        if form.is_valid():
            task_list = form.save(commit=False)
            task_list.board = board

            # Coloca la lista al final del tablero.
            last_position = (
                board.lists.order_by("-position")
                .values_list("position", flat=True)
                .first()
            )

            task_list.position = (
                last_position + 1
                if last_position is not None
                else 0
            )

            task_list.save()

            notify_board_members(
                board,
                (
                    f"{request.user.username} creó la lista "
                    f"'{task_list.title}' en el tablero '{board.title}'."
                ),
                exclude_user=request.user,
            )
            send_board_update(
                board.id,
                f"Se creó una nueva lista: {task_list.title}",
            )

            messages.success(
                request,
                "Lista creada correctamente.",
            )

            return redirect(
                "boards:board_detail",
                board_id=board.id,
            )

    else:
        form = TaskListForm()

    return render(
        request,
        "boards/list_form.html",
        {
            "form": form,
            "board": board,
        },
    )


@login_required
def list_update(request, list_id):
    """
    Edita una lista existente.

    Solo el propietario del tablero puede editarla.
    """

    task_list = get_object_or_404(
        TaskList,
        id=list_id,
        board__owner=request.user,
    )

    if request.method == "POST":
        form = TaskListForm(
            request.POST,
            instance=task_list,
        )

        if form.is_valid():
            updated_list = form.save()

            notify_board_members(
                updated_list.board,
                (
                    f"{request.user.username} actualizó la lista "
                    f"'{updated_list.title}' en el tablero '{updated_list.board.title}'."
                ),
                exclude_user=request.user,
            )   

            send_board_update(
                updated_list.board.id,
                f"Se actualizó la lista: {updated_list.title}",
            )

            messages.success(
                request,
                "Lista actualizada correctamente.",
            )

            return redirect(
                "boards:board_detail",
                board_id=updated_list.board.id,
            )

    else:
        form = TaskListForm(instance=task_list)

    return render(
        request,
        "boards/list_form.html",
        {
            "form": form,
            "board": task_list.board,
        },
    )


@login_required
def list_delete(request, list_id):
    """
    Elimina una lista del tablero.

    También elimina sus tarjetas mediante CASCADE.
    """

    task_list = get_object_or_404(
        TaskList,
        id=list_id,
        board__owner=request.user,
    )

    board = task_list.board
    board_id = board.id

    if request.method == "POST":
        list_title = task_list.title

        notify_board_members(
            board,
            (
                f"{request.user.username} eliminó la lista "
                f"'{list_title}' del tablero '{board.title}'."
            ),
            exclude_user=request.user,
        )

        task_list.delete()

        send_board_update(
            board_id,
            f"Se eliminó la lista: {list_title}",
        )

        messages.success(
            request,
            "Lista eliminada correctamente.",
        )

        return redirect(
            "boards:board_detail",
            board_id=board_id,
        )

    return render(
        request,
        "boards/list_delete.html",
        {
            "task_list": task_list,
        },
    )


@login_required
def card_create(request, list_id):
    """
    Crea una tarjeta dentro de una lista.

    Si la tarjeta tiene un usuario asignado,
    se genera una notificación para ese usuario.
    """

    task_list = get_object_or_404(
        TaskList,
        id=list_id,
        board__owner=request.user,
    )

    if request.method == "POST":
        form = CardForm(
            request.POST,
            task_list=task_list,
        )

        if form.is_valid():
            card = form.save(commit=False)
            card.task_list = task_list

            # Coloca la tarjeta al final de la lista.
            last_position = (
                task_list.cards.order_by("-position")
                .values_list("position", flat=True)
                .first()
            )

            card.position = (
                last_position + 1
                if last_position is not None
                else 0
            )

            card.save()

            board = task_list.board
            action_message = (
                f"{request.user.username} creó la tarjeta "
                f"'{card.title}' en la lista '{task_list.title}' "
                f"del tablero '{board.title}'."
            )

            notify_board_members(
                board,
                action_message,
                exclude_user=request.user,
            )

            send_board_update(
                board.id,
                action_message,
            )

            messages.success(
                request,
                "Tarjeta creada correctamente.",
            )

            return redirect(
                "boards:board_detail",
                board_id=task_list.board.id,
            )

    else:
        form = CardForm(
            task_list=task_list,
        )

    return render(
        request,
        "boards/card_form.html",
        {
            "form": form,
            "task_list": task_list,
        },
    )


@login_required
def card_update(request, card_id):
    """
    Edita una tarjeta existente.

    Si cambia el usuario asignado, se genera una
    notificación para el nuevo responsable.
    """

    card = get_object_or_404(
        Card,
        id=card_id,
        task_list__board__owner=request.user,
    )

    previous_assigned_user_id = card.assigned_to_id

    if request.method == "POST":
        form = CardForm(
            request.POST,
            instance=card,
            task_list=card.task_list,
        )

        if form.is_valid():
            updated_card = form.save()

            board = updated_card.task_list.board
            action_message = (
                f"{request.user.username} actualizó la tarjeta "
                f"'{updated_card.title}' en el tablero "
                f"'{board.title}'."
            )

            notify_board_members(
                board,
                action_message,
                exclude_user=request.user,
            )

            send_board_update(
                board.id,
                action_message,
            )

            messages.success(
                request,
                "Tarjeta actualizada correctamente.",
            )

            return redirect(
                "boards:board_detail",
                board_id=board.id,
            )

    else:
        form = CardForm(
            instance=card,
            task_list=card.task_list,
        )

    return render(
        request,
        "boards/card_form.html",
        {
            "form": form,
            "task_list": card.task_list,
        },
    )


@login_required
def card_delete(request, card_id):
    """
    Elimina una tarjeta.

    Si tenía un usuario asignado, se le notifica
    que la tarea fue eliminada.
    """

    card = get_object_or_404(
        Card,
        id=card_id,
        task_list__board__owner=request.user,
    )

    board = card.task_list.board
    board_id = board.id

    if request.method == "POST":
        card_title = card.title
        assigned_user = card.assigned_to

        action_message = (
            f"{request.user.username} eliminó la tarjeta "
            f"'{card_title}' del tablero '{board.title}'."
        )

        notify_board_members(
            board,
            action_message,
            exclude_user=request.user,
        )

        card.delete()

        send_board_update(
            board_id,
            action_message,
        )

        messages.success(
            request,
            "Tarjeta eliminada correctamente.",
        )

        return redirect(
            "boards:board_detail",
            board_id=board_id,
        )

    return render(
        request,
        "boards/card_delete.html",
        {
            "card": card,
        },
    )


@login_required
@require_POST
def reorder_lists(request):
    """
    Guarda el nuevo orden de las listas mediante Drag & Drop.
    """

    try:
        data = json.loads(request.body)
        list_ids = data.get("list_ids", [])

        if not list_ids:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "No se recibieron listas.",
                },
                status=400,
            )

        first_list = get_object_or_404(
            TaskList,
            id=list_ids[0],
            board__owner=request.user,
        )

        board = first_list.board

        valid_lists = TaskList.objects.filter(
            id__in=list_ids,
            board=board,
        )

        if valid_lists.count() != len(list_ids):
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Una o más listas no son válidas.",
                },
                status=400,
            )

        with transaction.atomic():
            for index, list_id in enumerate(list_ids):
                TaskList.objects.filter(
                    id=list_id,
                    board=board,
                ).update(position=index)

        send_board_update(
            board.id,
            (
                f"{request.user.username} modificó "
                f"el orden de las listas."
            ),
        )

        return JsonResponse(
            {
                "status": "ok",
            }
        )

    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse(
            {
                "status": "error",
                "message": "Datos inválidos.",
            },
            status=400,
        )


@login_required
@require_POST
def reorder_cards(request):
    """
    Guarda el nuevo orden de las tarjetas mediante Drag & Drop.
    """

    try:
        data = json.loads(request.body)

        list_id = data.get("list_id")
        card_ids = data.get("card_ids", [])

        task_list = get_object_or_404(
            TaskList,
            id=list_id,
            board__owner=request.user,
        )

        valid_cards = Card.objects.filter(
            id__in=card_ids,
            task_list=task_list,
        )

        if valid_cards.count() != len(card_ids):
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Una o más tarjetas no son válidas.",
                },
                status=400,
            )

        with transaction.atomic():
            for index, card_id in enumerate(card_ids):
                Card.objects.filter(
                    id=card_id,
                    task_list=task_list,
                ).update(position=index)

        send_board_update(
            task_list.board.id,
            (
                f"{request.user.username} modificó el orden "
                f"de las tarjetas en la lista '{task_list.title}'."
            ),
        )

        return JsonResponse(
            {
                "status": "ok",
            }
        )

    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse(
            {
                "status": "error",
                "message": "Datos inválidos.",
            },
            status=400,
        )