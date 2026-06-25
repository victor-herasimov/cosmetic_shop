"""
Модуль що містить моделі електронних адрес.
"""

from django.db import models
from . import SiteConfig


class Email(models.Model):
    """
    Модель для збереження електронних адрес компанії або сайту.

    Використовується для відображення контактних даних у різних частинах сайту
    (наприклад, у футері) та для керування їхньою активністю.
    """

    email = models.EmailField(verbose_name="Email")
    in_footer = models.BooleanField(default=True, verbose_name="Показувати в футері")
    active = models.BooleanField(default=True, verbose_name="Активний")

    config = models.ForeignKey(
        SiteConfig,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="emails",
    )

    def __str__(self) -> str:
        """Повертає текстове представлення моделі (саму електронну адресу)."""
        return f"{self.email}"

    class Meta:
        """Мета-параметри моделі для конфігурації додатка та відображення в адмін-панелі."""

        app_label = "main"
        verbose_name = "Email"
        verbose_name_plural = "Emails"
