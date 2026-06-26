"""
Реєстрація та конфігурація сторінки політики повернення в адмін-панелі.
"""

from django.contrib import admin
from pages.models import ReturnPolicy
from .base import BaseLegalDocumentAdmin


@admin.register(ReturnPolicy)
class ReturnPolicyAdmin(BaseLegalDocumentAdmin):
    """
    Адміністративна панель для керування сторінкою 'Повернення та обмін'.

    Повністю успадковує інтерфейс, структуру полів та синглтон-поведінку
    від `BaseLegalDocumentAdmin`.
    """
