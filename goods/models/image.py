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

    def clean(self):
        if self.is_main:
            dupes = Foto.objects.filter(product=self.product).exclude(pk=self.pk)
            print(dupes)
            if dupes.filter(is_main=True).exists():
                print(dupes)
                raise ValidationError(
                    "Для цього батьківського об'єкта вже існує основний запис."
                )

    def save(self, *args, **kwargs):
        self.clean()
        if self.is_main:
            Foto.objects.filter(product=self.product).exclude(pk=self.pk).update(
                is_main=False
            )

        super().save(*args, **kwargs)
