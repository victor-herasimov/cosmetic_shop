"""
Модуль для реалізації бізнес-логіки обробки відгуків.

Забезпечує сервісний шар (ReviewService) для створення, оновлення
та управління відгуками користувачів про товари.
"""

from typing import Any

from review.models import Review
from account.models import User as CustomUser


class ReviewService:
    """Сервіс для управління відгуками про товари."""

    model = Review

    @classmethod
    def get(cls, user: CustomUser, product_id: int) -> Review | None:
        try:
            review: Review = Review.objects.get(user=user, product_id=product_id)
            return review
        except Review.DoesNotExist:
            return None

    @classmethod
    def update_or_create(
        cls, user: CustomUser, product_id: int, data: dict[str, Any]
    ) -> tuple[Review, bool]:
        """Створює новий або оновлює існуючий відгук користувача.

        Args:
            user (CustomUser): Авторизований користувач, який залишає відгук.
            data (dict[str, Any]): Словник із валідованими даними форми
                (очікуються ключі 'product', 'rating', 'text').

        Returns:
            tuple[Review, bool]: Кортеж із екземпляром Review та прапорцем created.
        """

        review, created = cls.model.objects.update_or_create(
            user=user,
            product_id=product_id,
            defaults={"rating": data["rating"], "text": data["text"]},
        )

        return review, created
