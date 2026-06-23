"""
Модуль налаштування панелі адміністратора для керування замовленнями (Order).

Цей файл конфігурує відображення замовлень, інформації про клієнтів,
статусів оплати/доставки, а також підключає вбудовані позиції товарів у замовленні.
"""

from decimal import Decimal

from django.contrib import admin
from django.db import models, transaction
from django.utils.html import format_html
from order.models import Order
from order.models.order_item import OrderItem
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
        """Визначаємо кольори для різних статусів"""
        colors: dict[str, dict[str, str]] = {
            "new": {"bg": "#e0f7fa", "text": "#006064"},
            "in_progress": {"bg": "#fff3e0", "text": "#e65100"},
            "shipped": {"bg": "#e8eaf6", "text": "#1a237e"},
            "completed": {"bg": "#e8f5e9", "text": "#1b5e20"},
            "delivered": {"bg": "#e1f5fe", "text": "#01579b"},
            "canceled": {"bg": "#ffebee", "text": "#b71c1c"},
        }

        bg_color = colors.get(obj.status).get("bg")

        text_color = colors.get(obj.status).get("text")

        return format_html(
            '<span style="background-color: {}; color: {}; padding: 5px 10px; border-radius: 4px; font-weight: bold;">{}</span>',
            bg_color,
            text_color,
            obj.get_status_display(),  # Відображає зрозумілу людині назву (verbose name)
        )

    save_on_top = True
    search_fields = ["email", "phone", "first_name", "last_name", "id"]
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

    def save_related(self, request, form, formsets, change):
        """
        Керування залишками товарів на складі після успішної валідації форми замовлення.
        """
        order = form.instance

        # Отримуємо старий статус з бази даних перед збереженням нових зв'язків
        old_status = None
        if change:
            old_status = (
                Order.objects.filter(pk=order.pk)
                .values_list("status", flat=True)
                .first()
            )

        # Зберігаємо інлайни через стандартний механізм Django
        super().save_related(request, form, formsets, change)

        # Статуси повернення на склад
        restocked_statuses = ["new", "canceled"]

        # Оскільки форми збережені, ми можемо безпечно перерахувати залишки на складі
        with transaction.atomic():
            for formset in formsets:
                if formset.model == OrderItem:
                    for item_form in formset.forms:
                        # Пропускаємо незаповнені форми
                        if not item_form.cleaned_data:
                            continue

                        product = item_form.cleaned_data.get("product")
                        new_qty = item_form.cleaned_data.get("quantity", 0)
                        is_deleted = item_form.cleaned_data.get("DELETE", False)

                        # Отримуємо значення кількості, яка була раніше збережена в базі для цього рядка
                        old_qty = 0
                        if item_form.instance.pk:
                            # Оскільки super().save_related() вже виконався, дістаємо первинні дані через pre-saved стан або залишаємо логіку через відстеження змін:
                            old_qty = (
                                item_form.instance.quantity if not is_deleted else 0
                            )

                        if not product:
                            continue

                        # Сценарій 1: Статус змінився на Нове/Скасовано з активного -> Повертаємо ВСІ товари замовлення на склад
                        if (
                            change
                            and old_status not in restocked_statuses
                            and order.status in restocked_statuses
                        ):
                            product.count = models.F("count") + new_qty
                            product.save(update_fields=["count"])

                        # Сценарій 2: Статус змінився з Нове/Скасовано на активний (В обробці тощо) -> Списуємо ВСІ товари
                        elif (
                            change
                            and (old_status in restocked_statuses or old_status is None)
                            and order.status not in restocked_statuses
                        ):
                            product.count = models.F("count") - new_qty
                            product.save(update_fields=["count"])

                        # Сценарій 3: Статус НЕ змінювався (залишився активним), але змінилась КІЛЬКІСТЬ окремого товару
                        elif order.status not in restocked_statuses:
                            # Шукаємо фактичну дельту (ми використовуємо збереження змінної до super() якщо потрібно,
                            # або розраховуємо зміну на основі поточної форми)
                            if item_form.initial:
                                db_old_qty = item_form.initial.get("quantity", 0)
                                if is_deleted:
                                    # Якщо товар видалили з активного замовлення -> повертаємо на склад
                                    product.count = models.F("count") + db_old_qty
                                else:
                                    # Різниця між тим що стало і тим що було
                                    diff = new_qty - db_old_qty
                                    product.count = models.F("count") - diff
                                product.save(update_fields=["count"])
