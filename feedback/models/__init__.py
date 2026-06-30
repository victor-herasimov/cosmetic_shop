"""
Ініціалізаційний модуль моделей додатка FeedBack.

Експортує основні моделі для роботи з FeedBack,
забезпечуючи чисті імпорти виду `from feedback.models import Feedback`.
"""

from .feedback import Feedback

__all__ = ["Feedback"]
