"""
Vistas principales del sistema.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    """
    Dashboard principal.
    """

    return render(
        request,
        "boards/dashboard.html"
    )