from django.db import models

from mixins import SlugMixin, DateMixin


class Category(SlugMixin, DateMixin):
    name = models.CharField(max_length=256, unique=True, verbose_name="Назва категорії")
    short_description = models.CharField(max_length=25, verbose_name="Опис")

    class Meta:
        app_label = "goods"
        verbose_name = "Категорію"
        verbose_name_plural = "Категорії"
        ordering = ["-name"]

    def __str__(self):
        return f"{self.name}"
