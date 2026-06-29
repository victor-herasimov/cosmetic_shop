"""Модуль що містить моделі Графіка роботи"""

from django.db import models


class WorkSchedule(models.Model):
    """Модель графіка роботи."""

    schedule = models.CharField(max_length=512, verbose_name="Графік")

    def __str__(self) -> str:
        """Рядкове представлення графіка роботи."""
        return f"{self.schedule}"

    class Meta:
        """Мета-параметри моделі графіка роботи."""

        verbose_name = "Графік роботи"
        verbose_name_plural = "Графік роботи"
