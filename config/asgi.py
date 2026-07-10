"""
Configuración ASGI del proyecto SGT.

Permite atender solicitudes HTTP y conexiones WebSocket
mediante Django Channels.
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# Configuración de Django antes de importar rutas que usan aplicaciones.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Inicializa Django y su registro de aplicaciones.
django_asgi_app = get_asgi_application()

# Se importa después de inicializar Django.
from apps.realtime.routing import websocket_urlpatterns


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
    }
)
