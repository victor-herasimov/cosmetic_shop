"""
Модуль для управління обраними товарами користувачів.

Цей модуль визначає модель `Favorite`, яка забезпечує зв'язок
«багато-до-багатьох» між користувачами та товарами для збереження
списку улюблених позицій.
"""

from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Product
from account.models import User as CustomUser


User: type[CustomUser] = get_user_model()


class Favorite(models.Model):
    """
    Модель для опису обраного товару користувача (Wishlist).
    Забезпечує унікальне зв'язування між користувачем та товаром.
    Запобігає дублюванню одного й того самого товару в списку обраного
    одного користувача.

    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="favorites"
    )

    class Meta:
        """Метадані моделі Обраного."""

        unique_together = ("user", "product")
        verbose_name = "Улюблений товар"
        verbose_name_plural = "Улюблені товари"

    def __str__(self) -> str:
        """Повертає строкове представлення об'єкта обраного товару."""
        return f"{self.user.email} — {self.product.title}"
