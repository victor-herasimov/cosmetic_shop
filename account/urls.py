"""
Модуль маршрутизації (URL-конфігурація) для додатка account.

Визначає точки доступу (endpoints) для керування користувачами.
"""

from django.urls import URLResolver, path
from account.views import LoginView


app_name: str = "account"

urlpatterns: list[URLResolver] = [
    path("create/", LoginView.as_view(), name="login"),
]
