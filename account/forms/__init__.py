"""
Пакет кастомних форм автентифікації користувачів.

Цей модуль експортує готові форми для авторизації та реєстрації,
забезпечуючи чистий інтерфейс імпорту (Public API) для інших додатків.
"""

from .login import EmailOrPhoneLoginForm
from .register import UserRegistrationForm

__all__ = ["EmailOrPhoneLoginForm", "UserRegistrationForm"]
