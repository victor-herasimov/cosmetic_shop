"""
Модуль для обробки та збереження замовлень клієнтів.

Містить основну модель замовлення, яка консолідує дані про покупця,
обраний спосіб доставки, адресу, загальну вартість та поточний статус
обробки замовлення в системі. Також модуль відповідає за автоматичне
керування залишками товарів на складі при зміні статусів замовлень.
"""

from django.contrib import admin
from order.forms import OrderItemInlineFormSet
from order.models import OrderItem
from order.models.order import Order


class OrderItemInline(admin.TabularInline):
    """
    Інлайн-відображення для керування позиціями товарів у замовленні.

    Забезпечує можливість додавання, редагування та видалення товарів
    безпосередньо на сторінці детального перегляду замовлення, а також
    автоматично обмежує права редагування залежно від статусу замовлення.
    """

    model = OrderItem
    formset = OrderItemInlineFormSet

    def get_cost(self, obj):
        """
        Обчислює та повертає текстове представлення повної вартості позиції.

        Для нових (ще не збережених у базі) об'єктів повертає прочерк.
        """
        if not obj.id is None:
            return f"{obj.get_cost()}"
        return "-"

    get_cost.short_description = "Вартість: "

    fields = ["product", "price", "quantity", "get_cost"]
    readonly_fields = ["get_cost", "price"]
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        """
        Динамічно змінює доступність полів інлайну для редагування.

        Якщо замовлення вже створене (obj не None) і його статус
        відмінний від 'new' (Нове), то поля стають доступними тільки для читання.
        """
        # Якщо це створення нового замовлення (obj ще немає в базі), дозволяємо редагувати все
        if obj is None:
            return super().get_readonly_fields(request, obj)

        # Якщо статус замовлення вже НЕ "новий"
        current_db_status = (
            Order.objects.filter(pk=obj.pk).values_list("status", flat=True).first()
        )

        if current_db_status not in ["new"]:
            return ["product", "quantity", "price", "get_cost"]

        return super().get_readonly_fields(request, obj)

    def has_add_permission(self, request, obj=None):
        """Забороняє додавати нові товари в інлайн, якщо статус не new"""
        current_db_status = (
            Order.objects.filter(pk=obj.pk).values_list("status", flat=True).first()
        )
        if current_db_status != "new":
            return False
        return super().has_add_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """Забороняє видаляти існуючі товари з інлайну, якщо статус не new."""
        current_db_status = (
            Order.objects.filter(pk=obj.pk).values_list("status", flat=True).first()
        )
        if current_db_status != "new":
            return False
        return super().has_delete_permission(request, obj)
