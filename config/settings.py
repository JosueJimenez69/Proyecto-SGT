from pathlib import Path  # Permite manejar rutas del proyecto de forma ordenada.

BASE_DIR = Path(__file__).resolve().parent.parent  # Ruta base del proyecto.

SECRET_KEY = 'django-insecure-cambiar-en-produccion'  # Clave de seguridad para desarrollo.

DEBUG = True  # Activa modo desarrollo.

ALLOWED_HOSTS = []  # Hosts permitidos durante desarrollo.

INSTALLED_APPS = [
    'django.contrib.admin',  # Panel administrativo de Django.
    'django.contrib.auth',  # Sistema de autenticación.
    'django.contrib.contenttypes',  # Manejo de tipos de contenido.
    'django.contrib.sessions',  # Manejo de sesiones.
    'django.contrib.messages',  # Sistema de mensajes.
    'django.contrib.staticfiles',  # Archivos estáticos.

    'rest_framework',  # Django REST Framework.
    'channels',  # Django Channels para WebSockets.

    'apps.accounts',  # App de usuarios.
    'apps.boards',  # App de tableros, listas y tarjetas.
    'apps.notifications',  # App de notificaciones.
    'apps.realtime',  # App de tiempo real.
]

ASGI_APPLICATION = 'config.asgi.application'  # Configuración ASGI para Channels.

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Motor de templates.
        'DIRS': [BASE_DIR / 'templates'],  # Carpeta global de templates.
        'APP_DIRS': True,  # Permite templates dentro de cada app.
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # Permite acceder a request.
                'django.contrib.auth.context_processors.auth',  # Permite acceder al usuario.
                'django.contrib.messages.context_processors.messages',  # Permite mensajes.
            ],
        },
    },
]

STATIC_URL = 'static/'  # Ruta pública de archivos estáticos.
STATICFILES_DIRS = [BASE_DIR / 'static']  # Carpeta static del proyecto.

LOGIN_URL = 'login'  # Redirige aquí si el usuario no inició sesión.
LOGIN_REDIRECT_URL = 'dashboard'  # Redirige al dashboard luego del login.
LOGOUT_REDIRECT_URL = 'login'  # Redirige al login luego del logout.