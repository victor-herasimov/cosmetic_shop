"""
Модуль бізнес-логіки (сервісного шару) для роботи із способами доставки.
"""

from django.db.models import QuerySet

from order.models import DeliveryMethod


class DeliveryMethodService:
    """
    Сервіс для керування життєвим циклом доставки.
    """

    @classmethod
    def get_actives(cls) -> QuerySet[DeliveryMethod]:
        """
        Повертає всі способи доставки.
        """
        return DeliveryMethod.objects.filter(is_active=True)

    @classmethod
    def get_active_first(cls) -> DeliveryMethod | None:
        """
        Повертає перший спосіб доставки.
        """
        return DeliveryMethod.objects.filter(is_active=True).first()
