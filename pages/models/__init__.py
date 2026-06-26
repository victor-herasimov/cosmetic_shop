"""
Пакет, що об'єднує всі моделі даних додатка документів таких як Плітика конфіденційності... (pages app).

Імпортує та експортує ключові конфігураційні,
забезпечуючи зручний доступ до них через один імпорт (наприклад, з `pages.models`).
"""

from .privacy_policy import PrivacyPolicy
from .delivery_and_pay import DeliveryAndPayPolicy
from .return_policy import ReturnPolicy

__all__ = [
    "PrivacyPolicy",
    "DeliveryAndPayPolicy",
    "ReturnPolicy",
]
