"""
Реєстрація та конфігурація сторінки політики конфіденційності в адмін-панелі.
"""

from django.contrib import admin
from pages.models import PrivacyPolicy
from .base import BaseLegalDocumentAdmin


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(BaseLegalDocumentAdmin):
    """
    Адміністративна панель для керування сторінкою 'Політика конфіденційності'.

    Повністю успадковує інтерфейс, структуру полів та синглтон-поведінку
    від `BaseLegalDocumentAdmin`.
    """
