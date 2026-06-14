"""
Configuración principal de URLs del proyecto SGT.
Aquí se conectan las rutas generales del sistema, el panel admin
y las rutas internas de cada aplicación.
"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    # Ruta del panel administrativo de Django.
    path('admin/', admin.site.urls),

    # Rutas de autenticación de Django.
    path('accounts/', include('django.contrib.auth.urls')),

    # Rutas de la app de tableros.
    path('', include('boards.urls')),
]