"""
Пакет кастомних форм автентифікації користувачів.

Цей модуль експортує готові форми для авторизації та реєстрації,
забезпечуючи чистий інтерфейс імпорту (Public API) для інших додатків.
"""

from .login import EmailOrPhoneLoginForm
from .register import UserRegistrationForm
from .password_reset import PasswordResetForm
from .change_name import ChangeUserNameForm

__all__ = [
    "EmailOrPhoneLoginForm",
    "UserRegistrationForm",
    "PasswordResetForm",
    "ChangeUserNameForm",
]
