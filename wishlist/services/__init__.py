"""
Ініціалізаційний модуль сервісного шару додатка улюблених товарір.

Експортує сервіси бізнес-логіки, дозволяючи іншим компонентам системи
використовувати чисті імпорти виду `from wishlist.services import FavoriteService`.
"""

from .favorite import FavoriteService


__all__ = ["FavoriteService"]
