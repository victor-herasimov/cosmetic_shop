"""
Модуль кастомних шаблонних тегів Django для роботи з адресами.

Цей модуль реєструє теги, які можна використовувати в HTML-шаблонах
для динамічного отримання адрес
безпосередньо через сервісний шар.
"""

from django import template
from django.db.models import QuerySet
from main.models import Address
from main.services import AddressService

register = template.Library()


@register.simple_tag
def get_addresses() -> QuerySet[Address]:
    """
    Шаблонний тег, що повертає всі адреси.
    """
    return AddressService.get_all()
