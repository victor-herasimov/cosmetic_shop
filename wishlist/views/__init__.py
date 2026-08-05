"""
Пакет представлень (views) для модуля улюблених товарів (wishlist).

Експортує класи для:
- Перемикання стану товару в обраному (ToggleFavoriteView)
- Відображення списку обраних товарів (FavoriteListView)
- Перенаправлення на сторінку обраного (FavoriteRedirectView)
"""

from .toggle import ToggleFavoriteView
from .favorite_list import FavoriteListView
from .favorite_redirect import FavoriteRedirectView

__all__ = ["ToggleFavoriteView", "FavoriteListView", "FavoriteRedirectView"]
