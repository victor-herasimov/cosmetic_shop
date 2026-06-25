"""
Пакет, що об'єднує всі моделі даних головного додатка (main app).

Імпортує та експортує ключові конфігураційні, контентні та контактні моделі,
забезпечуючи зручний доступ до них через один імпорт (наприклад, з `apps.main.models`).
"""

from .strip import Strip
from .site_config import SiteConfig
from .hero import Hero
from .email import Email
from .phones import Phone
from .socials import Social
from .privacy_policy import PrivacyPolicy
from .delivery_and_pay import DeliveryAndPayPolicy
from .return_policy import ReturnPolicy

__all__ = [
    "Strip",
    "SiteConfig",
    "Hero",
    "Email",
    "Phone",
    "Social",
    "PrivacyPolicy",
    "DeliveryAndPayPolicy",
    "ReturnPolicy",
]
