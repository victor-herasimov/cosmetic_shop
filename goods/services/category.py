from django.db.models import Count, QuerySet

from goods.models import Category


class CategoryService:
    @classmethod
    def get_all(cls) -> QuerySet[Category]:
        return Category.objects.all()

    @classmethod
    def get_all_with_count_products(cls) -> QuerySet[Category]:
        return Category.objects.annotate(product_count=Count("products"))

    @classmethod
    def get_category_by_slug(cls, slug: str) -> Category:
        return Category.objects.get(slug=slug)
