"""
Модуль кастомних шаблонних тегів Django для роботи з даними телефону.

Цей модуль реєструє теги, які можна використовувати в HTML-шаблонах
для динамічного отримання контактної інформації (телефонних номерів)
безпосередньо через сервісний шар.
"""

from django import template
from main.models import Phone
from main.services import PhoneService

register = template.Library()


@register.simple_tag
def get_first_active_phone() -> Phone:
    """
    Шаблонний тег, що повертає перший активний номер телефону.
    """
    return PhoneService.get_first_active_phone()
