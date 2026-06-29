"""
Модуль сервісів для роботи з адресами.
"""

from django.db.models import QuerySet

from main.models import Address


class AddressService:
    """
    Сервіс для керування та отримання даних про адреси.

    Ізолює бізнес-логіку та запити до бази даних, пов'язані з
    моделлю Address, забезпечуючи чисту архітектуру додатку.
    """

    @classmethod
    def get_all(cls) -> QuerySet[Address]:
        """
        Повертає відсортований список усіх адрес із бази даних.
        """
        return Address.objects.order_by("address").all()
