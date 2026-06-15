from collections.abc import Iterable

from django.db.models import Count, TextField, Value
from django.db.models.functions import Concat
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from goods.models import Product
from goods.models.category import Category


class ProductService:
    def get_all(self, order: str | None = None) -> QuerySet[Product]:
        """
        Повертає кверісет з усіма продуктами
        """
        result = (
            Product.objects.select_related("cateogry").prefetch_related("fotos").all()
        )
        if order:
            result = result.order_by(order)
        return result

    def get_by_id(self, product_id: int) -> Product:
        """
        Повертає товар по йго ID.
        """
        return Product.objects.get(id=product_id)

    def get_products_by_category(
        self, category: Category, order: str | None = None
    ) -> QuerySet[Product]:
        """
        Повертає кверісет з усіма продуктами за категорією.
        """
        result = (
            Product.objects.select_related("cateogry")
            .prefetch_related("fotos")
            .filter(cateogry=category)
        )
        if order:
            result = result.order_by(order)
        return result

    def get_products_count(self) -> int:
        """
        Повертає кількість усіх товарів.
        """
        return Product.objects.count()

    def get_bestsellers(self) -> QuerySet[Product]:
        """
        Повертає кверісет з першими 4-ма продуктами, що є хітом продаж. Якщо таких менше 4-х
        то добавляє іншими продуктами.
        """
        return (
            Product.objects.select_related("cateogry")
            .prefetch_related("fotos")
            .order_by("-is_bestseller", "-updated")[:4]
        )

    def get_news(self) -> QuerySet[Product]:
        """
        Повертає кверісет з першими 4-ма новими продуктами.
        """
        return (
            Product.objects.select_related("cateogry")
            .prefetch_related("fotos")
            .order_by("-is_new", "-created")[:4]
        )

    def get_by_slug(self, slug: str) -> Product:
        """
        Повертає Продукт, що відповідє слагу. Якщо такого не має то викидає виключення Product.DoesNotExist.
        """
        return (
            Product.objects.select_related("cateogry")
            .prefetch_related("fotos", "characteristics__item")
            .get(slug=slug)
        )

    def search(self, query, order: str | None = None) -> QuerySet[Product]:
        """
        Повертає прдукти, що містять запит query в заголовку або описі.
        """
        if len(query) > 0:
            results = (
                Product.objects.annotate(
                    search_text=Concat(
                        "title", Value(" "), "description", output_field=TextField()
                    )
                )
                .annotate(similarity=TrigramSimilarity("search_text", query))
                .filter(similarity__gt=0.007)
                .order_by("-similarity")
            )
            if order:
                results = results.order_by(order)
            return results

        return Product.objects.none()

    def get_similar_products(self, product_slug: str) -> QuerySet[Product]:
        """
        Повертає продукти, що подібні до продукта в якого слаг дорівнює product_slug.
        """
        product = get_object_or_404(Product, slug=product_slug)
        current_char_ids = product.characteristics.values_list("id", flat=True)

        similar_products = (
            Product.objects.filter(characteristics__in=current_char_ids)
            .exclude(id=product.id)
            .annotate(same_chars_count=Count("characteristics"))
            .order_by("-same_chars_count", "?")
            .select_related("cateogry")
            .prefetch_related("characteristics__item", "fotos")[:4]
        )
        return similar_products

    def get_products_by_ids(self, ids: Iterable[int]) -> QuerySet[Product]:
        """
        Повертає кверісет з продуктів id яких міститься в списку ids.
        """
        return Product.objects.prefetch_related("fotos").filter(id__in=ids)
