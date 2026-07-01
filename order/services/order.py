"""
Модуль бізнес-логіки (сервісного шару) для роботи із замовленнями.
"""

from typing import Any

from django.db import transaction
from django.http import HttpRequest

from cart.cart import Cart
from goods.models import Product
from order.models import Order
from order.tasks import send_order_notification_task
from .order_item import OrderItemService


class OrderService:
    """
    Сервіс для керування життєвим циклом замовлень.
    """

    def __init__(self, request: HttpRequest, data: dict[str, Any]) -> None:
        """Ініціалізація сервісу замовлень"""
        self.cart = Cart(request)
        self.data = data
        self.base_url = f"{request.scheme}://{request.get_host()}"

    def _create(self) -> Order:
        return Order.objects.create(**self.data)

    def _send_order_notifications(self, order_id: int) -> None:
        """Надсилає листи менеджеру і клієнту."""
        send_order_notification_task.delay(order_id, self.base_url)

    def _process_cart(self, order: Order) -> None:
        """Зберігає товари з кошика в базі даних і очищає кошик"""
        for item in self.cart:
            product: Product = item["product"]
            OrderItemService.create(
                order=order,
                product=product,
                price=item["price"],
                quantity=item["quantity"],
            )
        self.cart.clear()

    def create_order(self) -> Order:
        """
        Створює нове замовлення на основі поточного кошика користувача.

        Бере товари з кошика, фіксує їхню вартість,
        створює запис в базі даних та очищує кошик.
        """
        if not self.cart:
            raise ValueError("Неможливо створити замовлення з порожнім кошиком.")

        with transaction.atomic():
            order: Order = self._create()
            self._process_cart(order)

            transaction.on_commit(lambda: self._send_order_notifications(order.id))

        return order
