"""
Модуль бізнес-логіки (сервісного шару) для роботи із замовленнями.
"""

from typing import Any

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Prefetch, QuerySet
from django.http import HttpRequest

from account.models import User as CustomUser
from cart.cart import Cart
from goods.models import Product
from order.models import Order
from order.models.order_item import OrderItem
from order.tasks import send_order_notification_task
from .order_item import OrderItemService


User: type[CustomUser] = get_user_model()


class OrderService:
    """
    Сервіс для керування життєвим циклом замовлень.
    """

    def __init__(
        self, request: HttpRequest, data: dict[str, Any] | None = None
    ) -> None:
        """Ініціалізація сервісу замовлень"""
        self.cart = Cart(request)
        self.data: dict[str, Any] = data
        self.request: HttpRequest = request
        self.base_url: str = f"{self.request.scheme}://{self.request.get_host()}"

    def _create(self) -> Order | None:
        """Створює замовлення"""
        if not self.data:
            return None
        user: CustomUser = (
            self.request.user if self.request.user.is_authenticated else None
        )
        return Order.objects.create(user=user, **self.data)

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

    def get_orders_for_authenticated_user(
        self, status_filter: str | None = None
    ) -> QuerySet[Order]:
        """Повертає замовлення для залогіненого користувача"""
        if not self.request.user.is_authenticated:
            raise PermissionDenied(
                "Спроба отримати замовлення неавторизованим користувачем."
            )

        queryset = Order.objects.filter(user=self.request.user)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return (
            queryset.select_related("delivery_method", "payment_method")
            .prefetch_related(
                Prefetch(
                    "items",
                    queryset=OrderItem.objects.select_related(
                        "product__cateogry"
                    ).prefetch_related("product__fotos"),
                )
            )
            .order_by("-created")
        )
