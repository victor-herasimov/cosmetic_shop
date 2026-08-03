"""
Модуль для управління списком обраних товарів користувача
"""

from django.http import HttpRequest
from django.http import Http404

from goods.models import Product
from wishlist.models import Favorite


class FavoriteService:
    """Сервісний клас для управління списком обраних товарів користувача.

    Інкапсулює бізнес-логіку додавання та видалення товарів із списку обраного
    (wishlist) на основі поточного HTTP-запиту.

    Attributes:
        request (HttpRequest): Об'єкт поточного HTTP-запиту Django.
    """

    def __init__(self, request: HttpRequest) -> None:
        """Ініціалізує FavoriteService екземпляром HttpRequest.

        Args:
            request (HttpRequest): Об'єкт HTTP-запиту, що містить інформацію
                про поточного користувача (request.user).
        """
        self.request: HttpRequest = request

    def toggle(self, product_id: int) -> bool:
        """
        Перемикає статус товару в обраному для поточного користувача.

        Якщо товар вже є в списку обраного користувача, він видаляється звідти.
        Якщо товару немає — він додається до списку.
        """

        if not Product.objects.filter(pk=product_id).exists():
            raise Http404("Товар не знайдено.")

        favorite, created = Favorite.objects.get_or_create(
            user=self.request.user, product_id=product_id
        )
        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True

        return is_favorite

    def has_favorite(self) -> bool:
        """
        Повертає True якщо користувач авторизований і має улюблені,
        інакше False.
        """
        is_favorite: bool = False
        if self.request.user.is_authenticated:
            is_favorite = Favorite.objects.filter(user=self.request.user).exists()

        return is_favorite
