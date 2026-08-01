"""
Модуль для обробки та збереження замовлень клієнтів.

Містить основну модель замовлення, яка консолідує дані про покупця,
обраний спосіб доставки, адресу, загальну вартість та поточний статус
обробки замовлення в системі.
"""

from decimal import Decimal
import re

from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.core.validators import ValidationError
from goods.models.product import Product
from mixins import DateMixin
from validators import PhoneNumberValidator
from account.models import User as CustomUser
from .delivery_method import DeliveryMethod
from .payment_method import PaymentMethod


User: type[CustomUser] = get_user_model()


class Order(DateMixin):
    """
    Модель замовлення в інтернет-магазині.
    """

    class Status(models.TextChoices):
        """Перелік можливих статусів замовлення в системі."""

        NEW = "new", "Новe"
        IN_PROGRESS = "in_progress", "В обробці"
        SHIPPED = "shipped", "Відправлено"
        DELIVERED = "delivered", "Доставлено"
        COMPLETED = "completed", "Виконано"
        CANSELED = "canceled", "Відмінено"

    status = models.CharField(
        max_length=11,
        verbose_name="Статус замовлення",
        choices=Status,
        default=Status.NEW,
    )
    first_name = models.CharField(max_length=256, verbose_name="Ім'я")
    last_name = models.CharField(max_length=256, verbose_name="Прізвище")
    phone = models.CharField(
        max_length=19,
        verbose_name="Телефон",
        unique=False,
        validators=[PhoneNumberValidator()],
    )
    email = models.EmailField(verbose_name="Email", unique=False)

    user = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        null=True,
        blank=True,
        default=None,
        verbose_name="Користувач",
    )

    delivery_method = models.ForeignKey(
        DeliveryMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        verbose_name="Спосіб доставки",
    )

    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        verbose_name="Спосіб оплати",
    )

    city = models.CharField(max_length=128, verbose_name="Місто")
    delivery_address = models.CharField(max_length=512, verbose_name="Адреса доставки")
    comment = models.TextField(blank=True, null=True, verbose_name="Коментар")

    class Meta:
        """Мета-параметри моделі замовлення (назви в адмінці, сортування та індекси)."""

        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self) -> str:
        """
        Повертає рядкове представлення замовлення.
        """
        return f"Замовлення {self.id}"

    def get_total_cost(self) -> Decimal:
        """
        Обчислює загальну вартість замовлення.
        """
        return sum(item.get_cost() for item in self.items.all())

    def get_clean_phone(self) -> str:
        """
        Очищає номер телефону від форматування, видаляючи дужки, дефіси.

        Корисно для генерації клікабельних посилань виду 'tel:+380...' в HTML-шаблонах.
        """
        return re.sub(r"[\s/(/)/-]", "", self.phone)

    def save(self, *args, **kwargs) -> None:
        """
        Зберігає замовлення в базу даних з перевіркою зміни статусу.
        """
        if self.pk:
            old_order: Order = Order.objects.get(pk=self.pk)
            if (
                old_order
                and old_order.status in ("new", "canceled")
                and self.status not in ("new", "canceled")
            ):
                with transaction.atomic():
                    for item in self.items.select_related("product").all():
                        product: Product = item.product
                        if product.count < item.quantity:
                            raise ValidationError(
                                f"Недостатньо товару {product.title} на складі! "
                                f"Доступно: {product.count}, потрібно: {item.quantity}."
                            )
                        Product.objects.filter(pk=product.pk).update(
                            count=models.F("count") - item.quantity
                        )
            if (
                old_order
                and old_order.status not in ("new", "canceled")
                and self.status in ("canceled", "new")
            ):
                with transaction.atomic():
                    for item in self.items.select_related("product").all():
                        product: Product = item.product
                        Product.objects.filter(pk=product.pk).update(
                            count=models.F("count") + item.quantity
                        )

        return super().save(*args, **kwargs)
