"""Пакет для аутентифікації та керування сесіями користувачів.

Експортує:
    LoginView: Клас представлення для авторизації користувачів.
"""

from .login import LoginView
from .logout import LogoutView
from .register import RegisterView
from .password_reset import PasswordResetView
from .password_reset_confirm import AsyncPasswordResetConfirmView
from .account_settings import AccountSettingsView
from .change_name import ChangeUserNameView
from .change_email import ChangeUserEmailView
from .change_phone import ChangeUserPhoneView
from .change_password import ChangeUserPasswordView
from .delete import DeleteUserView
from .orders import UserOrderList

__all__ = [
    "LoginView",
    "LogoutView",
    "RegisterView",
    "PasswordResetView",
    "AsyncPasswordResetConfirmView",
    "AccountSettingsView",
    "ChangeUserNameView",
    "ChangeUserEmailView",
    "ChangeUserPhoneView",
    "ChangeUserPasswordView",
    "DeleteUserView",
    "UserOrderList",
]
