"""
Ініціалізаційний модуль сервісного шару додатка замовлень.

Експортує сервіси бізнес-логіки, дозволяючи іншим компонентам системи
використовувати чисті імпорти виду `from orders.services import OrderService`.
"""

from .order import OrderService


__all__ = ["OrderService"]
