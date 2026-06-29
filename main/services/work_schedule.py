"""
Модуль сервісів для роботи з графіком роботи.
"""

from django.db.models import QuerySet

from main.models import WorkSchedule


class WorkScheduleService:
    """
    Сервіс для керування та отримання даних про графіки роботи.

    Ізолює бізнес-логіку та запити до бази даних, пов'язані з
    моделлю WorkSchedle, забезпечуючи чисту архітектуру додатку.
    """

    @classmethod
    def get_all(cls) -> QuerySet[WorkSchedule]:
        """
        Повертає відсортований список усіх графіків роботи із бази даних.
        """
        return WorkSchedule.objects.order_by("schedule").all()
