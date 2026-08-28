"""
Модуль для реалізації бізнес-логіки обробки відгуків.

Забезпечує сервісний шар (ReviewService) для створення, оновлення
та управління відгуками користувачів про товари.
"""

from typing import Any

from django.db import DatabaseError

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
    def delete(cls, review_id: int, user: CustomUser) -> bool:
        """
        Видаляє відгук за його ID, якщо він належить вказаному користувачу.

        Args:
            review_id (int): Унікальний ідентифікатор відгуку.
            user (CustomUser): Об'єкт користувача, який намагається видалити відгук.

        Returns:
            bool: True, якщо відгук успішно знайдено та видалено.
                  False, якщо відгук не існує, не належить користувачу або виникла помилка.
        """
        try:
            review: Review = cls.model.objects.get(id=review_id, user=user)
            review.delete()
            return True
        except (cls.model.DoesNotExist, DatabaseError):
            return False

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
