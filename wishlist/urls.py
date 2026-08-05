"""
Модуль маршрутизації (URL-конфігурація) для додатка улюблених.

Визначає точки доступу (endpoints) для керування процесом додавання, видалення і відображення улюблених
товарів.
"""

from django.urls import URLResolver, path
from wishlist.views import ToggleFavoriteView, FavoriteListView, FavoriteRedirectView


app_name: str = "wishlist"

urlpatterns: list[URLResolver] = [
    path("favorites/", FavoriteListView.as_view(), name="favorite"),
    path(
        "favorites-redirect/", FavoriteRedirectView.as_view(), name="favorite_redirect"
    ),
    path("toggle/<int:product_id>/", ToggleFavoriteView.as_view(), name="toggle"),
]
