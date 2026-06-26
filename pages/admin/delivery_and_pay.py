"""
Реєстрація та конфігурація сторінки доставки та оплати в адмін-панелі.
"""

from django.contrib import admin
from pages.models import DeliveryAndPayPolicy
from .base import BaseLegalDocumentAdmin


@admin.register(DeliveryAndPayPolicy)
class DeliveryAndPayPolicyAdmin(BaseLegalDocumentAdmin):
    """
    Адміністративна панель для керування сторінкою 'Доставка та оплата'.

    Повністю успадковує інтерфейс, структуру полів та синглтон-поведінку
    від `BaseLegalDocumentAdmin`.
    """
