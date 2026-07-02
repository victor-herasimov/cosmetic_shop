"""
Модуль для продукта.
"""

from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import strip_tags
from meta.models import ModelMeta
from mixins import DateMixin, SlugMixin
from .category import Category
from .characteristic import Characteristic


class Product(ModelMeta, DateMixin, SlugMixin):
    """
    Модель продукта
    """

    title = models.CharField(max_length=512, verbose_name="Заголовок")
    cateogry = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категорія",
    )

    description = CKEditor5Field("Опис", config_name="extends")
    method_apply = CKEditor5Field(
        "Спосіб застосування",
        config_name="extends",
        blank=True,
        null=True,
        default=None,
    )

    composition = models.TextField(
        verbose_name="Склад", null=True, blank=True, default=None
    )

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

    is_bestseller = models.BooleanField(
        default=False,
        verbose_name="Хіт продаж",
        help_text='Відображаються на головній сторінці в розділі "Улюбленці покупців" і позначаються бейджом "Хіт".',
    )
    is_new = models.BooleanField(
        default=True,
        verbose_name="Новинка",
        help_text='Відображаються на головній сторінці в розділі "Щойно з`явилися" і позначаються бейджом "Новинка".',
    )

    characteristics = models.ManyToManyField(
        Characteristic,
        blank=True,
        default=None,
        related_name="books",
        verbose_name="Характеристики",
    )

    vegan_frendly = models.BooleanField(
        default=False,
        verbose_name="Vegan friendly, без жорстокості",
        help_text="Відображається на сторінці детальної інформації в розділі 'Переваги.'",
    )
    derma = models.BooleanField(
        default=False,
        verbose_name="Дерматологічно протестовано",
        help_text="Відображається на сторінці детальної інформації в розділі 'Переваги.'",
    )
    delivery = models.BooleanField(
        default=False,
        verbose_name="Доставка по всій Україні 1–3 дні",
        help_text="Відображається на сторінці детальної інформації в розділі 'Переваги.'",
    )

    active = models.BooleanField(
        default=False,
        verbose_name="Активні рослинні компоненти",
        help_text="Відображається на сторінці детальної інформації в розділі 'Переваги.'",
    )

    class Meta:
        app_label = "goods"
        ordering = ["title"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["-created"]),
            GinIndex(
                name="product_title_trgm_idx",
                fields=["title"],
                opclasses=["gin_trgm_ops"],
            ),
            GinIndex(
                name="product_desc_trgm_idx",
                fields=["description"],
                opclasses=["gin_trgm_ops"],
            ),
        ]
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"

    _metadata = {
        "title": "title",
        "description": "get_seo_description",
        "image": "get_image_url",
        "og_type": "product",
    }

    def get_seo_description(self) -> str:
        """Повертає перші 150 символів опису для SEO"""
        if not self.description:
            return ""
        return strip_tags(str(self.description))[:150] + "..."

    def get_image_url(self):
        first_foto = self.fotos.first()
        if first_foto:
            return first_foto.image.url
        return None

    @property
    def available(self) -> bool:
        """
        Повертає True, якщо продукт є в наявності.
        """
        return self.count > 0

    @property
    def has_benefits(self) -> bool:
        """
        Повертає True, якщо продукт має переваги.
        """
        return self.vegan_frendly or self.derma or self.delivery or self.active

    @property
    def is_discount(self) -> bool:
        """
        Повертає True, якщо продукт має знижку.
        """
        return self.discount > 0

    @property
    def get_price_with_discount(self) -> Decimal:
        """
        Повертає ціну продукту з урахуванням знижки.
        """
        return self.price * Decimal((1 - self.discount / 100))

    def get_absolute_url(self):
        """
        Повертає url для продукту.
        """
        return reverse("goods:product", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        """
        Повертає текстове представлення продукту.
        """
        return f"{self.title}"
