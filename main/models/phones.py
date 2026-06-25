"""
Цей модуль містить моделі для збереження та валідації номерів телефонів та їхнього зв'язку з глобальною конфігурацією сайту (SiteConfig).
"""

import re
from django.db import models

from validators import PhoneNumberValidator

from . import SiteConfig


class Phone(models.Model):
    """
    Модель для збереження телефонних номерів компанії або сайту.

    Використовується для відображення контактів у різних секціях (наприклад, у футері),
    підтримує валідацію формату та має метод для очищення номера від зайвих символів.
    """

    phone = models.CharField(
        max_length=19, verbose_name="Телефон", validators=[PhoneNumberValidator()]
    )
    in_footer = models.BooleanField(default=True, verbose_name="Показувати в футері")
    active = models.BooleanField(default=True, verbose_name="Активний")

    config = models.ForeignKey(
        SiteConfig,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="phones",
    )

    def __str__(self) -> str:
        """Повертає текстове представлення моделі (сам номер телефону)."""
        return f"{self.phone}"

    def clean_number(self) -> str:
        """
        Очищає номер телефону від форматування, видаляючи дужки, дефіси.

        Корисно для генерації клікабельних посилань виду 'tel:+380...' в HTML-шаблонах.
        """
        return re.sub(r"[/(/)/-]", "", self.phone)

    class Meta:
        """Мета-параметри для відображення моделі в адмін-панелі Django."""

        app_label = "main"
        verbose_name = "Телефон"
        verbose_name_plural = "Телефони"
