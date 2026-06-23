"""
Модуль для керування способами оплати в інтернет-магазині.
"""

from django.db import models


class PaymentMethod(models.Model):
    """
    Модель, що представляє спосіб оплати товарів.
    """

    title = models.CharField(max_length=100, verbose_name="Назва способу оплати")
    short_description = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        default=None,
        verbose_name="Короткий опис",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активний")

    def __str__(self):
        """Повертає текстове представлення способу оплати."""
        return f"{self.title}"

    class Meta:
        app_label = "order"
        ordering = ["title"]
        verbose_name = "Спосіб оплати"
        verbose_name_plural = "Способи оплати"
