from django.db.models import QuerySet

from goods.models import Product
from goods.models.category import Category


class ProductService:
    def get_all(self) -> QuerySet[Product]:
        """
        Повертає кверісет з усіма продуктами
        """
        return (
            Product.objects.select_related("cateogry").prefetch_related("fotos").all()
        )

    def get_products_by_category(self, category: Category) -> QuerySet[Product]:
        """
        Повертає кверісет з усіма продуктами за категорією.
        """
        return (
            Product.objects.select_related("cateogry")
            .prefetch_related("fotos")
            .filter(cateogry=category)
            .order_by("-updated")
        )

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
