"""
Configuración ASGI del proyecto SGT.

Este archivo permite que Django soporte WebSockets
y funcionalidades en tiempo real mediante Channels.
"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

# Define el archivo principal de configuración.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Aplicación Django para peticiones HTTP.
django_asgi_app = get_asgi_application()

# Router principal ASGI.
application = ProtocolTypeRouter({
    "http": django_asgi_app,
})