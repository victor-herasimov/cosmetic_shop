"""Модуль що містить моделі Графіка роботи"""

from django.db import models

from .site_config import SiteConfig


class WorkSchedule(models.Model):
    """Модель графіка роботи."""

    schedule = models.CharField(max_length=512, verbose_name="Графік")
    config = models.ForeignKey(
        SiteConfig,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="schedules",
    )

    def __str__(self) -> str:
        """Рядкове представлення графіка роботи."""
        return f"{self.schedule}"

    class Meta:
        """Мета-параметри моделі графіка роботи."""

        verbose_name = "Графік роботи"
        verbose_name_plural = "Графік роботи"
