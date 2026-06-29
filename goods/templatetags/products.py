from django import template
from django.db.models import QuerySet
from django.utils.http import urlencode

from goods.models.product import Product
from goods.services.product import ProductService


register = template.Library()


@register.simple_tag
def get_product_news() -> QuerySet[Product]:
    return ProductService.get_news()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs) -> str:
    query = context["request"].GET.dict()
    query.update(kwargs)
    return urlencode(query)
