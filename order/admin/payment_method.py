"""
Модуль налаштування панелі адміністратора для методів оплати (PaymentMethod).
"""

from django.contrib import admin
from order.models import PaymentMethod


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    """
    Налаштування адмін-панелі для методів оплати (PaymentMethod).
    """

    list_display = ["title", "is_active"]
    list_display_links = ["title"]

    fields = ["title", "is_active", "short_description"]
    readonly_fields = ["id"]
