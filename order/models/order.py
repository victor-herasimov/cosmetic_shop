"""
Модуль для обробки та збереження замовлень клієнтів.

Містить основну модель замовлення, яка консолідує дані про покупця,
обраний спосіб доставки, адресу, загальну вартість та поточний статус
обробки замовлення в системі.
"""

from django.db import models
from mixins import DateMixin
from validators import PhoneNumberValidator
from .delivery_method import DeliveryMethod
from .payment_method import PaymentMethod


class Order(DateMixin):
    """
    Модель замовлення в інтернет-магазині.
    """

    class Status(models.TextChoices):
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

    delivery_method = models.ForeignKey(
        DeliveryMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Спосіб доставки",
    )

    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Спосіб оплати",
    )

    city = delivery_address = models.CharField(max_length=128, verbose_name="Місто")
    delivery_address = models.CharField(max_length=512, verbose_name="Адреса доставки")
    comment = models.TextField(blank=True, null=True, verbose_name="Коментар")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Закази"
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"Заказ {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
