from django import template
from django.db.models import QuerySet
from goods.models.category import Category
from goods.services import CategoryService

register = template.Library()


@register.simple_tag
def get_visible_categories() -> QuerySet[Category]:
    category_servise: CategoryService = CategoryService()
    return category_servise.get_visible()
