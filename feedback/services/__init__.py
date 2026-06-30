"""
Ініціалізаційний модуль сервісного шару додатка Зворотнього зв`язку.

Експортує сервіси бізнес-логіки, дозволяючи іншим компонентам системи
використовувати чисті імпорти виду `from feedback.services import FeedbackService`.
"""

from .feedback import FeedbackService

__all__ = ["FeedbackService"]
