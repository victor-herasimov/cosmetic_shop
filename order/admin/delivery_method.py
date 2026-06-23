"""
Модуль налаштування панелі адміністратора для керування способами доставки (DeliveryMethod).

Цей файл конфігурує відображення, доступність та структуру полів для
редагування варіантів доставки товарів покупцям.
"""

from django.contrib import admin
from order.models import DeliveryMethod


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    """
    Конфігурація адмін-панелі для моделі Спосіб доставки (DeliveryMethod).
    """

    list_display = ["title", "is_active"]
    list_display_links = ["title"]

    fields = ["title", "is_active", "short_description"]
    readonly_fields = ["id"]
