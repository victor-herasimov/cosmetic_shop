"""
Ініціалізаційний модуль сервісного шару додатка замовлень.

Експортує сервіси бізнес-логіки, дозволяючи іншим компонентам системи
використовувати чисті імпорти виду `from orders.services import OrderService`.
"""

from .order import OrderService
from .delivery_method import DeliveryMethodService
from .payment_method import PaymentMethodService


__all__ = ["OrderService", "DeliveryMethodService", "PaymentMethodService"]
