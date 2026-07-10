"""
Configuración principal del proyecto SGT.
Aquí se definen las apps instaladas, base de datos, templates, archivos static,
autenticación, Django REST Framework y Channels.
"""

from pathlib import Path

# Ruta base del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta del proyecto. En producción debe cambiarse.
SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'

# Modo desarrollo activado.
DEBUG = True

# Permite acceder desde cualquier host en desarrollo.
ALLOWED_HOSTS = ['*']


# Aplicaciones instaladas.
INSTALLED_APPS = [
    # Apps internas de Django.
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps externas necesarias para el proyecto.
    'rest_framework',
    'channels',

    # Apps del proyecto SGT.
    'apps.boards',
    'apps.accounts',
    'apps.notifications',
    'apps.realtime',
    'users',
]



# Middlewares del proyecto.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Archivo principal de rutas.
ROOT_URLCONF = 'config.urls'


# Configuración de templates.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Carpeta general de templates.
        'DIRS': [BASE_DIR / 'templates'],

        # Permite usar templates dentro de cada app.
        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Configuración WSGI para despliegues tradicionales.
WSGI_APPLICATION = 'config.wsgi.application'

# Configuración ASGI para soporte de Channels y WebSockets.
ASGI_APPLICATION = 'config.asgi.application'


# Base de datos SQLite para desarrollo.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validadores de contraseña.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Idioma del sistema.
LANGUAGE_CODE = 'es-py'

# Zona horaria de Paraguay.
TIME_ZONE = 'America/Asuncion'

USE_I18N = True
USE_TZ = True


# Archivos estáticos.
STATIC_URL = '/static/'

# Carpeta static general del proyecto.
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Carpeta donde Django recopila archivos estáticos en producción.
STATIC_ROOT = BASE_DIR / 'staticfiles'


# Tipo de ID automático por defecto.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Configuración de autenticación.
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'


# Configuración básica de correo para desarrollo.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Configuración básica de Django REST Framework.
REST_FRAMEWORK = {}


# Configuración básica de Channels.
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}