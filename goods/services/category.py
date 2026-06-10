from django.db.models import QuerySet

from goods.models import Category


class CategoryService:
    def get_all(self) -> QuerySet[Category]:
        return Category.objects.all()

    def get_visible(self) -> QuerySet[Category]:
        return Category.objects.filter(visible=True)
