"""
Модуль для опису моделей товарів (goods), які використовуються в системі.

Містить модель Brand.
"""

from django.db import models

from mixins import SlugMixin, DateMixin


class Brand(SlugMixin, DateMixin):
    """
    Модель для представлення бренду товару.

    Успадковує функціонал автоматичного створення slug (SlugMixin)
    та фіксації дат створення/оновлення запису (DateMixin).
    """

    name = models.CharField(max_length=256, unique=True, verbose_name="Назва бренду")

    class Meta:
        """Мета-налаштування для моделі Brand."""

        app_label = "goods"
        verbose_name = "Бренд"
        verbose_name_plural = "Бренди"
        ordering = ["-name"]

    def __str__(self):
        """Повертає строкове представлення бренду (його назву)."""
        return f"{self.name}"
