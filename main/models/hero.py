"""
Моделі даних для головного додатка (main app).

Цей модуль містить контентну модель, яка відповідає за
динамічне наповнення першого екрана сайту (Hero секція).
"""

import os
from django.db import models
from solo.models import SingletonModel


class Hero(SingletonModel):
    """
    Синглтон-модель для керування контентом головного банера (Hero секції) сайту.

    Містить заголовки, описи, зображення та плашки (бейджи), які зазвичай
    відображаються на першому екрані головної сторінки. Оскільки це SingletonModel,
    у базі даних може існувати лише один екземпляр цього класу.
    """

    title = models.CharField(
        max_length=50,
        default="Догляд, що повертає шкірі сяйво",
        verbose_name="Заголовок (великий)",
    )
    subtitle = models.CharField(
        max_length=35,
        default="Краса доступна кожному",
        verbose_name="Заголовок (маленький)",
    )
    short_description = models.CharField(
        max_length=125,
        blank=True,
        null=True,
        default=None,
        verbose_name="Короткий опис",
    )
    image = models.ImageField(
        blank=True, null=True, upload_to="hero", verbose_name="Картинка"
    )

    badge_title = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default=None,
        verbose_name="Заголовок (бейдж)",
    )
    badge_value = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default=None,
        verbose_name="Значення (бейдж)",
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        """Мета-параметри для відображення моделі в адмін-панелі Django."""

        app_label = "main"
        verbose_name: str = "Hero секція"

    def __str__(self) -> str:
        """Повертає текстове представлення — великий заголовок секції."""
        return f"{self.title}"

    def save(self, *args, **kwargs):
        """
        Зберігає зміни в моделі та автоматично видаляє старе зображення з диска,
        якщо воно було замінене на нове.
        """
        if self.pk:
            try:
                old_config = Hero.objects.get(pk=self.pk)
                if old_config.image and old_config.image != self.image:
                    if os.path.isfile(old_config.image.path):
                        os.remove(old_config.image.path)
            except Hero.DoesNotExist:
                pass

        super().save(*args, **kwargs)
