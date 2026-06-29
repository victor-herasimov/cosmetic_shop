from django.db.models import QuerySet
from django.http import HttpRequest

from goods.models.category import Category

from .services import CategoryService


def all_categories(request: HttpRequest) -> dict[str, QuerySet[Category]]:
    return {"all_categories": CategoryService.get_all()}
