from django.db import models
from mixins import DateMixin
from .product import Product


class Information(DateMixin):
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Опис")

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="informations",
        verbose_name="Продукт",
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Інформацію"
        verbose_name_plural = "Інформація"
