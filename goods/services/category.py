from django.db.models import Count, QuerySet

from goods.models import Category


class CategoryService:
    def get_all(self) -> QuerySet[Category]:
        return Category.objects.all()

    def get_visible(self) -> QuerySet[Category]:
        return Category.objects.filter(visible=True)

    def get_all_with_count_products(self) -> QuerySet[Category]:
        return Category.objects.annotate(product_count=Count("products"))

    def get_category_by_slug(self, slug: str) -> Category:
        return Category.objects.get(slug=slug)
