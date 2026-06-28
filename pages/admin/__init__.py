"""
Пакет конфігурацій адмін-панелі для юридичних та інформаційних сторінок.

Об'єднує та експортує класи налаштувань Django Admin (такі як політика
конфіденційності, правила повернення, умови доставки та оплати),
забезпечуючи чистий імпорт через інтерфейс пакета.
"""

from .delivery_and_pay import DeliveryAndPayPolicyAdmin
from .privacy_policy import PrivacyPolicyAdmin
from .return_policy import ReturnPolicyAdmin
from .public_offer import PublicOfferAdmin

__all__ = [
    "DeliveryAndPayPolicyAdmin",
    "PrivacyPolicyAdmin",
    "ReturnPolicyAdmin",
    "PublicOfferAdmin",
]
