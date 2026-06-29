"""
Модуль кастомних шаблонних тегів Django для роботи з графіками роботи.

Цей модуль реєструє теги, які можна використовувати в HTML-шаблонах
для динамічного отримання графіків роботи
безпосередньо через сервісний шар.
"""

from django import template
from django.db.models import QuerySet
from main.models import WorkSchedule
from main.services import WorkScheduleService

register = template.Library()


@register.simple_tag
def get_first_active_phone() -> QuerySet[WorkSchedule]:
    """
    Шаблонний тег, що повертає всі графіки роботи.
    """
    return WorkScheduleService.get_all()
