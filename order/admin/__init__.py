"""
Пакет налаштування адмін-панелі для модуля замовлень (Order).
"""

from .order import OrderAdmin
from .delivery_method import DeliveryMethodAdmin

from .payment_method import PaymentMethodAdmin

__all__: list[str] = ["OrderAdmin", "DeliveryMethodAdmin", "PaymentMethodAdmin"]
