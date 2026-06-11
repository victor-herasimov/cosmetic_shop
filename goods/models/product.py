from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from mixins import DateMixin, SlugMixin
from .category import Category
from .characteristic import Characteristic


class Product(DateMixin, SlugMixin):
    title = models.CharField(max_length=512, verbose_name="Заголовок")
    cateogry = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категорія",
    )

    description = CKEditor5Field("Опис", config_name="extends")

    count = models.IntegerField(
        validators=[MinValueValidator(0)], verbose_name="Залишок", default=0
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        verbose_name="Знижка",
        default=0,
    )

    characteristics = models.ManyToManyField(
        Characteristic,
        blank=True,
        default=None,
        related_name="books",
        verbose_name="Характеристики",
    )

    class Meta:
        app_label = "goods"
        ordering = ["title"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["title"]),
            models.Index(fields=["-created"]),
        ]
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"

    @property
    def available(self) -> bool:
        return self.count > 0

    @property
    def is_discount(self) -> bool:
        return self.discount > 0

    @property
    def get_price_with_discount(self) -> Decimal:
        return self.price * Decimal((1 - self.discount / 100))

    def __str__(self) -> str:
        return f"{self.title}"
