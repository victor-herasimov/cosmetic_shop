"""
Модуль для відображення сторінки списку улюблених товарів (wishlist).
"""

from typing import Any

from django.db.models import QuerySet
from django.views.generic import ListView

from goods.services import ProductService
from mixins.htmx_login_required_mixin import HTMXLoginRequiredMixin


class FavoriteListView(HTMXLoginRequiredMixin, ListView):
    """
    Представлення для відображення списку улюблених товарів.
    """

    template_name = "wishlist/wishlist.html"
    context_object_name = "products"

    def get_queryset(self):
        """
        Повертає відфільтрований список товарів для каталогу.
        """
        self.product_service = ProductService(self.request)
        return self.product_service.get_favorites()

    def get_context_data(self, **kwargs):
        """
        Доповнює контекст шаблону кількістю улюблених товарів.
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)
        products = context[self.context_object_name]
        context["favorites_count"] = (
            len(products) if isinstance(products, (list, QuerySet)) else 0
        )

        return context
