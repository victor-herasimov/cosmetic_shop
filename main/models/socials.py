"""
Модуль що містить моделі соціальних мереж.
"""

from django.db import models
from . import SiteConfig


class Social(models.Model):
    """
    Модель для збереження посилань на соціальні мережі компанії.

    Використовується для виведення посилань на офіційні сторінки
    у різних частинах сайту (наприклад, у футері) та керування їхньою активністю.
    """

    title = models.CharField(max_length=125, verbose_name="Соціальна мережа")
    url = models.URLField(max_length=255, verbose_name="URL")
    in_footer = models.BooleanField(default=True, verbose_name="Показувати в футері")
    active = models.BooleanField(default=True, verbose_name="Активний")

    config = models.ForeignKey(
        SiteConfig,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="socials",
    )

    def __str__(self) -> str:
        """Повертає текстове представлення моделі (назву соціальної мережі)."""
        return f"{self.title}"

    class Meta:
        """Мета-параметри для відображення моделі в адмін-панелі Django."""

        app_label = "main"
        verbose_name = "Соціальну мережу"
        verbose_name_plural = "Соціальні мережі"
