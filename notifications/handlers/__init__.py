"""Пакет для роботи зі сповіщеннями.

Цей модуль об'єднує різні обробники сповіщень (Email, SMS тощо) та надає
зручний інтерфейс для їх імпорту.
"""

from .email import EmailNotificationHandler
from .base import BaseNotificationHandler

__all__: list[str] = ["BaseNotificationHandler", "EmailNotificationHandler"]
