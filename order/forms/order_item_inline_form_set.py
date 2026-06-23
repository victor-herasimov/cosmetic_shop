"""
Цей модуль містить набір форм для валідації залишків на складі з урахуванням зміни статусів та кількості.
"""

from django.forms.models import BaseInlineFormSet
from order.models import OrderItem
from order.models.order import Order


class OrderItemInlineFormSet(BaseInlineFormSet):
    """
    Кастомний набір форм для валідації залишків на складі
    з урахуванням зміни статусів та кількості.
    """

    def clean(self):
        """
        Проводить комплексну валідацію кожної позиції товару в замовленні.

        Аналізує поточний стан замовлення в базі даних та порівнює його з новими
        значеннями кількості й статусу, які надіслав користувач. У разі дефіциту
        товару додає відповідну помилку валідації до конкретного поля форми.
        """

        super().clean()

        # Визначаємо новий статус замовлення, який обрав користувач в адмінці
        new_status = self.instance.status

        # Визначаємо старий статус, який зараз збережений в базі даних
        old_status = None
        if self.instance.pk:
            old_status = (
                Order.objects.filter(pk=self.instance.pk)
                .values_list("status", flat=True)
                .first()
            )

        # Статуси, при яких товар НЕ списується (знаходиться на складі)
        restocked_statuses = ["new", "canceled"]

        for form in self.forms:
            if not form.is_valid() or (form.cleaned_data.get("DELETE", False)):
                continue

            product = form.cleaned_data.get("product")
            new_quantity = form.cleaned_data.get("quantity", 0)

            if not product:
                continue

            # Поточна кількість товару безпосередньо на складі
            available_stock = (
                product.count
            )  # Припускаємо, що поле називається count або stock

            # Отримуємо стару кількість цього товару в замовленні (якщо воно редагується)
            old_quantity = 0
            if form.instance.pk:
                old_quantity = (
                    OrderItem.objects.filter(pk=form.instance.pk)
                    .values_list("quantity", flat=True)
                    .first()
                    or 0
                )

            # 1. Логіка: Перехід з "повернутого" статусу в "активний" (наприклад, з Нового в В обробці)
            if (
                old_status in restocked_statuses or old_status is None
            ) and new_status not in restocked_statuses:
                if new_quantity > available_stock:
                    form.add_error(
                        "quantity",
                        f"Недостатньо товару на складі! Доступно: {available_stock}. Необхідно: {new_quantity}.",
                    )

            # 2. Логіка: Замовлення вже було активним, і ми просто збільшуємо кількість товару
            elif (
                old_status not in restocked_statuses
                and new_status not in restocked_statuses
            ):
                added_quantity = new_quantity - old_quantity
                if added_quantity > 0 and added_quantity > available_stock:
                    form.add_error(
                        "quantity",
                        f"Не настільки багато товару на складі! Можна додати ще максимум: {available_stock}.",
                    )
