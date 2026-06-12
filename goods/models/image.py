from django.db import models
from django.forms import ValidationError
from mixins import DateMixin
from .product import Product


class Foto(DateMixin):
    image = models.ImageField(
        null=True, blank=True, upload_to="products", verbose_name="Фото"
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name="Головне фото",
        help_text="Може бути тільки одне для продукта",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="fotos",
        verbose_name="Фотографії",
    )

    class Meta:
        app_label = "goods"
        ordering = ["-is_main", "-updated"]
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    def __str__(self) -> str:
        return f"Foto {self.pk}"
