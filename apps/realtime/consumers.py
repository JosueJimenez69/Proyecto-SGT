"""
Consumers para manejar actualizaciones de tableros mediante WebSockets.
"""

import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q


class BoardConsumer(AsyncWebsocketConsumer):
    """
    Consumer del tablero.

    Solo permite la conexión de usuarios autenticados que sean
    propietarios o miembros del tablero solicitado.
    """

    async def connect(self):
        """Valida al usuario antes de aceptar la conexión."""

        self.board_id = self.scope["url_route"]["kwargs"]["board_id"]
        self.room_group_name = f"board_{self.board_id}"
        self.joined_group = False

        user = self.scope.get("user")

        if user is None or user.is_anonymous:
            await self.close(code=4401)
            return

        has_access = await self.user_has_board_access(
            user.id,
            self.board_id,
        )

        if not has_access:
            await self.close(code=4403)
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        self.joined_group = True

        await self.accept()

    async def disconnect(self, close_code):
        """Retira el canal del grupo cuando la conexión termina."""

        if self.joined_group:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )

    async def board_update(self, event):
        """Envía al navegador una actualización recibida del grupo."""

        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                }
            )
        )

    @database_sync_to_async
    def user_has_board_access(self, user_id, board_id):
        """Comprueba en la base de datos el acceso al tablero."""

        # Importación local para evitar cargar modelos antes de que
        # Django termine de inicializar el registro de aplicaciones.
        # pyrefly: ignore [missing-import]
        from apps.boards.models import Board

        return Board.objects.filter(
            Q(id=board_id, owner_id=user_id)
            | Q(id=board_id, members__id=user_id)
        ).exists()
