"""
Реєстрація та конфігурація сторінки публічної оферти в адмін-панелі.
"""

from django.contrib import admin
from pages.models import PublicOffer
from .base import BaseLegalDocumentAdmin


@admin.register(PublicOffer)
class PublicOfferAdmin(BaseLegalDocumentAdmin):
    """
    Адміністративна панель для керування сторінкою 'Публічноа оферта'.

    Повністю успадковує інтерфейс, структуру полів та синглтон-поведінку
    від `BaseLegalDocumentAdmin`.
    """
