"""
Модуль маршрутизації (URL-конфігурація) для додатка замовлень.

Визначає точки доступу (endpoints) для керування процесом купівлі.
"""

from django.urls import URLResolver, path
from order.views import OrderView


app_name: str = "checkout"

urlpatterns: list[URLResolver] = [path("", OrderView.as_view(), name="create")]
