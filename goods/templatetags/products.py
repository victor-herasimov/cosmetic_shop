from django import template
from django.db.models import QuerySet

from goods.models.product import Product
from goods.services.product import ProductService

register = template.Library()


@register.simple_tag
def get_product_bestsellers() -> QuerySet[Product]:
    return ProductService().get_bestsellers()


@register.simple_tag
def get_product_news() -> QuerySet[Product]:
    return ProductService().get_news()
