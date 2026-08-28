"""
Модуль ініціалізації представлень (views) для роботи з відгуками.

Експортує основні Class-Based Views для обробки та відображення відгуків,
надаючи чистий публічний інтерфейс для імпорту в інші частини додатка.
"""

from .get_page import GetReviewPageView
from .create import ReviewCreateView
from .delete import ReviewDeleteView

__all__ = ["GetReviewPageView", "ReviewCreateView", "ReviewDeleteView"]
