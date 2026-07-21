from django.db.models import QuerySet
from django.http import HttpRequest

from goods.models.category import Category
from goods.models.product import Product
from goods.services.product import ProductService

from .services import CategoryService


def all_categories(request: HttpRequest) -> dict[str, QuerySet[Category]]:
    return {"all_categories": CategoryService.get_all()}


def product_bestsellers(request: HttpRequest) -> QuerySet[Product]:
    return {"product_bestsellers": ProductService(request.GET).get_bestsellers()}
