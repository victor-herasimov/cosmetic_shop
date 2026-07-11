"""
Модуль маршрутизації (URL-конфігурація) для додатка account.

Визначає точки доступу (endpoints) для керування користувачами.
"""

from django.urls import URLResolver, path
from account.views import (
    LoginView,
    LogoutView,
    RegisterView,
    PasswordResetView,
    AsyncPasswordResetConfirmView,
    AccountSettingsView,
)


app_name: str = "account"

urlpatterns: list[URLResolver] = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("settings/", AccountSettingsView.as_view(), name="settings"),
    path(
        "reset/<uidb64>/<token>/",
        AsyncPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
