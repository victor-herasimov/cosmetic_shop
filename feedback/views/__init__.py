"""
Ініціалізаційний модуль представлень (Views) додатка Зворотнього зв`язку.

Збирає та експортує класи представлень (CBV), забезпечуючи чистий
і зрозумілий імпорт для модуля маршрутизації (urls.py) виду
`from .views import FeedbackView`.
"""

from .feedback import FeedbackCreateView

__all__ = ["FeedbackCreateView"]
