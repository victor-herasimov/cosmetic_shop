"""
Модуль маршрутизації (URL-конфігурація) для додатка account.

Визначає точки доступу (endpoints) для керування користувачами.
"""

from django.urls import URLResolver, path
from account.views import LoginView, LogoutView, RegisterView


app_name: str = "account"

urlpatterns: list[URLResolver] = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
