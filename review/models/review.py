"""
Модуль для опису моделі відгуків у системі.

Містить модель `Review`, яка відповідає за збереження оцінок
та текстових коментарів користувачів до продуктів.
"""

from django.db import models
from django.contrib.auth import get_user_model

from mixins import DateMixin
from account.models import User as CustomUser
from goods.models import Product

User: type[CustomUser] = get_user_model()


class Review(DateMixin):
    """
    Модель для зберігання відгуків користувачів про продукти.

    Attributes:
        product (ForeignKey): Посилання на модель `Product`, до якого залишено відгук.
        user (ForeignKey): Посилання на користувача (`User`), який залишив відгук.
        rating (PositiveSmallIntegerField): Числова оцінка продукту (від 1 до 5).
        text (TextField): Текстовий зміст відгуку (максимум 1000 символів).
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Продукт",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Рейтинг"
    )
    text = models.TextField(max_length=1000, verbose_name="Відгук")

    class Meta:
        """Мета-параметри для відображення моделі в адмін-панелі Django."""

        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ["-created"]

    def __str__(self) -> str:
        """
        Повертає строкове представлення об'єкта відгуку.

        Returns:
            str: Рядок із датою створення та назвою продукту.
        """
        return f"{self.created} - {self.product.title}"
