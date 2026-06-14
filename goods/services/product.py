from django.db.models import QuerySet

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

    def search(self, search_text) -> QuerySet[Product]:
        if len(search_text) > 0:
            return (
                Product.objects.select_related("cateogry")
                .prefetch_related("fotos")
                .filter(title__icontains=search_text)
                .order_by("-is_bestseller", "-updated")
                .distinct()
            )

        return Product.objects.none()
