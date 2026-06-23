"""
Модуль для керування способами доставки в інтернет-магазині.
"""

from django.db import models


class DeliveryMethod(models.Model):
    """
    Модель, що представляє спосіб доставки товарів.

    Зберігає інформацію про назву сервісу, статус активності цього способу на сайті.
    """

    title = models.CharField(max_length=100, verbose_name="Назва способу доставки")
    short_description = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        default=None,
        verbose_name="Короткий опис",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активний")

    def __str__(self):
        """Повертає текстове представлення способу доставки."""
        return f"{self.title}"

    class Meta:
        app_label = "order"
        ordering = ["title"]
        verbose_name = "Спосіб доставки"
        verbose_name_plural = "Способи доставки"
