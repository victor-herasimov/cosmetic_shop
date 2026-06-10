import os
from django.db import models
from solo.models import SingletonModel


class Hero(SingletonModel):
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
        app_label = "main"
        verbose_name: str = "Hero секція"

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_config = Hero.objects.get(pk=self.pk)
                if old_config.image and old_config.image != self.image:
                    if os.path.isfile(old_config.image.path):
                        os.remove(old_config.image.path)
            except Hero.DoesNotExist:
                pass

        super().save(*args, **kwargs)
