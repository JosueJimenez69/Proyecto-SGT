# Sistema de Gestión de Tareas (SGT)

## Descripción

El Sistema de Gestión de Tareas (SGT) es una aplicación web desarrollada con Django que permite administrar proyectos mediante tableros, listas y tarjetas, facilitando el trabajo colaborativo entre varios usuarios.

## Funcionalidades

- Registro e inicio de sesión de usuarios.
- Creación, edición y eliminación de tableros.
- Administración de listas y tarjetas.
- Asignación de miembros a los tableros.
- Asignación de responsables a las tareas.
- Reordenamiento de listas y tarjetas mediante Drag & Drop.
- Notificaciones y actualización en tiempo real mediante WebSockets.

## Tecnologías utilizadas

- Python
- Django
- Django Channels
- Daphne
- SQLite
- Bootstrap 5
- HTML, CSS y JavaScript
- Git y GitHub

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/JosueJimenez69/Proyecto-SGT.git
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Aplicar migraciones:

```bash
python manage.py migrate
```

Ejecutar el proyecto:

```bash
python manage.py runserver
```

Para utilizar WebSockets:

```bash
daphne config.asgi:application
```

## Integrantes

- Josué Jiménez.
- Alejandro Solalinde.
- Carlos Jara.

## Observación

El proyecto fue desarrollado con fines académicos para la asignatura de Programación V, utilizando Django bajo el patrón MVT, Git y GitHub para el control de versiones, WebSockets con Django Channels para la actualización en tiempo real y Drag & Drop para la organización dinámica de listas y tarjetas.