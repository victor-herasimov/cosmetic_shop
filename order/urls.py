"""
Модуль маршрутизації (URL-конфігурація) для додатка замовлень.

Визначає точки доступу (endpoints) для керування процесом купівлі.
"""

from django.urls import URLResolver, path
from order.views import OrderView, OrderSuccessView


app_name: str = "checkout"

urlpatterns: list[URLResolver] = [
    path("", OrderView.as_view(), name="create"),
    path("success/<int:order_id>/", OrderSuccessView.as_view(), name="order_success"),
]
