"""
Модуль для представлення елементів замовлення в базі даних.

Містить модель, яка пов'язує конкретні товари з замовленнями,
а також зберігає інформацію про їхню кількість та ціну на момент купівлі.
"""

from decimal import Decimal

from django.db import models

from goods.models import Product
from .order import Order


class OrderItem(models.Model):
    """
    Модель, що представляє окремий товар у замовленні.

    Пов'язує модель продукту з замовленням і фіксує фінансові
    та кількісні показники на момент оформлення.
    """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="Замовлення"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="Продукт",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    class Meta:
        verbose_name = "Замовлений продукт"
        verbose_name_plural = "Замовлені продукти"

    def __str__(self) -> str:
        """Повертає рядкове представлення елемента замовлення."""
        return f"{self.id}"

    def get_cost(self) -> Decimal:
        """Обчислює загальну вартість цієї позиції в замовленні."""
        return self.price * self.quantity

    def save(self, *args, **kwargs) -> None:
        """Зберігає об'єкт у базі даних."""
        if not self.price:
            self.price = self.product.get_price_with_discount
        return super().save(*args, **kwargs)
