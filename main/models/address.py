"""Модуль що містить моделі Адреса"""

from django.db import models


class Address(models.Model):
    """Модель адреса."""

    address = models.CharField(max_length=512, verbose_name="Адрес")

    def __str__(self) -> str:
        """Рядкове представлення адресу."""
        return f"{self.address}"

    class Meta:
        """Мета-параметри моделі адреса."""

        verbose_name = "Адресс"
        verbose_name_plural = "Адресу"
