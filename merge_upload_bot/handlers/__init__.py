# bot/handlers/__init__.py

from .start import start_handler
from .settings import settings_handler
from .merge import merge_handler
from .status import status_handler
from .admin import admin_handler

__all__ = [
    "start_handler",
    "settings_handler",
    "merge_handler",
    "status_handler",
    "admin_handler",
]
