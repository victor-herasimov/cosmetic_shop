"""
Модуль налаштування панелі адміністратора для керування замовленнями (Order).

Цей файл конфігурує відображення замовлень, інформації про клієнтів,
статусів оплати/доставки, а також підключає вбудовані позиції товарів у замовленні.
"""

from decimal import Decimal

from django.contrib import admin
from django.utils.html import format_html
from order.models import Order
from .order_item import OrderItemInline


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Конфігурація адмін-панелі для моделі Замовлення (Order).

    Забезпечує:
    - Виведення детальної інформації про клієнта та загальну суму.
    - Фільтрацію за датою створення та поточним статусом замовлення.
    - Відображення списку замовлених товарів через `OrderItemInline`.
    - Захист системних полів (дати, ID, сума) від випадкового редагування.
    """

    def get_total_cost(self, obj: Order) -> Decimal:
        """
        Обчислює та повертає повну вартість всього замовлення.
        """
        return obj.get_total_cost()

    get_total_cost.short_description = "Сума: "

    @admin.display(description="Статус")
    def status_colored(self, obj):
        # Визначаємо кольори для різних статусів
        colors: dict[str, dict[str, str]] = {
            "new": {"bg": "#e0f7fa", "text": "#006064"},
            "in_progress": {"bg": "#fff3e0", "text": "#e65100"},
            "shipped": {"bg": "#e8eaf6", "text": "#1a237e"},
            "completed": {"bg": "#e8f5e9", "text": "#1b5e20"},
            "delivered": {"bg": "#e1f5fe", "text": "#01579b"},
            "canceled": {"bg": "#ffebee", "text": "#b71c1c"},
        }

        # Отримуємо колір для поточного статусу (або білий за замовчуванням)
        bg_color = colors.get(obj.status).get("bg")

        # Колір тексту (можна зробити темнішим для контрасту)
        text_color = colors.get(obj.status).get("text")

        # Повертаємо безпечний HTML-код із вбудованими стилями
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 5px 10px; border-radius: 4px; font-weight: bold;">{}</span>',
            bg_color,
            text_color,
            obj.get_status_display(),  # Відображає зрозумілу людині назву (verbose name)
        )

    save_on_top = True
    list_display = [
        "id",
        "first_name",
        "last_name",
        "phone",
        "email",
        "status_colored",
        "created",
    ]
    list_display_links = [
        "id",
        "first_name",
        "last_name",
        "phone",
        "email",
    ]
    readonly_fields = ["created", "updated", "id", "get_total_cost"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "id",
                    "status",
                    "first_name",
                    "last_name",
                    "phone",
                    "email",
                    "payment_method",
                    "delivery_method",
                    "city",
                    "delivery_address",
                    "comment",
                    "get_total_cost",
                ]
            },
        ),
        (
            "Дати",
            {
                "fields": [
                    (
                        "updated",
                        "created",
                    ),
                ]
            },
        ),
    ]
    list_filter = ["created", "status"]
    inlines = [OrderItemInline]
