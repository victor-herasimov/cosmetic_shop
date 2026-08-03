from django import template
from django.db.models import QuerySet

from goods.models.product import Product
from goods.services.product import ProductService


register = template.Library()


@register.simple_tag(takes_context=True)
def get_product_news(context, **kwargs) -> QuerySet[Product]:
    return ProductService(context["request"]).get_news()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs) -> str:
    query = context["request"].GET.copy()

    # Оновлюємо параметри
    for key, value in kwargs.items():
        if isinstance(value, list):
            query.setlist(key, value)
        else:
            query[key] = value
    return query.urlencode()
