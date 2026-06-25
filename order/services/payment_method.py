"""
Модуль бізнес-логіки (сервісного шару) для роботи із способами оплати.
"""

from django.db.models import QuerySet

from order.models import PaymentMethod


class PaymentMethodService:
    """
    Сервіс для керування життєвим циклом оплати.
    """

    @classmethod
    def get_actives(cls) -> QuerySet[PaymentMethod]:
        """
        Повертає всі способи оплати.
        """
        return PaymentMethod.objects.filter(is_active=True)

    @classmethod
    def get_active_first(cls) -> PaymentMethod | None:
        """
        Повертає перший активний спосіб оплати.
        """
        return PaymentMethod.objects.filter(is_active=True).first()
