"""
Модуль що містить моделі для елементів стрічки.
"""

from django.db import models


class Strip(models.Model):
    """
    Модель для збереження окремих елементів текстової або контентної стрічки.

    Використовується для створення списків елементів (наприклад, переваг, брендів,
    тегів або рухомих рядків), що виводяться на сайті, з можливістю сортування за алфавітом.
    """

    name = models.CharField(max_length=255, verbose_name="Елемент")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        """Мета-параметри для налаштування сортування та відображення в адмін-панелі."""

        app_label = "main"
        verbose_name: str = "Стрічку"
        verbose_name_plural: str = "Стрічки"
        ordering = ["name"]

    def __str__(self) -> str:
        """Повертає текстове представлення моделі — назву елемента стрічки."""
        return f"{self.name}"
