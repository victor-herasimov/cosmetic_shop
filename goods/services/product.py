from django.db.models import QuerySet

from goods.models import Product
from goods.models.category import Category


class ProductService:
    def get_all(self) -> QuerySet[Product]:
        """
        Повертає кверісет з усіма продуктами
        """
        return Product.objects.all()

    def get_products_by_category(self, category: Category) -> QuerySet[Product]:
        """
        Повертає кверісет з усіма продуктами за категорією.
        """
        return Product.objects.filter(cateogry=category).order_by("-updated")

    def get_products_count(self) -> int:
        """
        Повертає кількість усіх товарів.
        """
        return Product.objects.count()
