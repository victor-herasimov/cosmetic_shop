"""
Модуль бізнес-логіки (сервісного шару) для роботи із замовленнями.
"""

from typing import Any

from django.db import transaction
from django.http import HttpRequest

from cart.cart import Cart
from goods.models import Product

from main.models import SiteConfig
from main.services import AddressService, SiteConfigService, WorkScheduleService
from order.models import Order
from notifications.services import NotificationService
from notifications.handlers import EmailNotificationHandler
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

    def _send_order_notifications(self, order: Order) -> None:
        """Надсилає листи менеджеру і клієнту."""
        self._send_client_notification(order)
        self._send_manager_notification(order)

    def _send_client_notification(self, order: Order) -> None:
        """Надсилає лист про замовлення клієнту."""
        notifications_service: NotificationService = NotificationService(
            handlers=[EmailNotificationHandler()]
        )
        schedules = [str(item) for item in WorkScheduleService.get_all()]
        config: SiteConfig = SiteConfigService().get()
        address_service: AddressService = AddressService()
        context: dict[str, Any] = {
            "config": config,
            "order": order,
            "base_url": self.base_url,
            "schedule": ", ".join(schedules),
            "phones": config.phones.all(),
            "emails": config.emails.all(),
            "socials": config.socials.all(),
            "addresses": address_service.get_all(),
        }

        notifications_service.notify(
            template_name_text="order/emails/email-order-confirmation.txt",
            context=context,
            template_name_html="order/emails/email-order-confirmation.html",
            email=order.email,
            subject=f"Замовлення №{ order.id } підтверджено!",
        )

    def _send_manager_notification(self, order: Order) -> None:
        """Надсилає лист менеджеру про замовлення."""
        notifications_service: NotificationService = NotificationService(
            handlers=[EmailNotificationHandler()]
        )
        config: SiteConfig = SiteConfigService().get()
        address_service: AddressService = AddressService()
        context: dict[str, Any] = {
            "config": config,
            "order": order,
            "base_url": self.base_url,
            "phones": config.phones.all(),
            "emails": config.emails.all(),
            "socials": config.socials.all(),
            "addresses": address_service.get_all(),
        }

        notifications_service.notify(
            template_name_text="order/emails/email-admin-order.txt",
            context=context,
            template_name_html="order/emails/email-admin-order.html",
            email="admin@mybeauty.com",
            subject=f"НОВЕ ЗАМОВЛЕННЯ №{order.id} — {order.get_total_cost()} грн — {order.last_name}",
        )

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
        with transaction.atomic():
            order: Order = self._create()
            self._process_cart(order)

            transaction.on_commit(lambda: self._send_order_notifications(order))

        return order
