"""
Модуль для відображення сторінки списку улюблених товарів (wishlist).
"""

from typing import Any

from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView
from view_breadcrumbs import BaseBreadcrumbMixin

from goods.services import ProductService
from mixins.htmx_login_required_mixin import HTMXLoginRequiredMixin


class FavoriteListView(BaseBreadcrumbMixin, HTMXLoginRequiredMixin, ListView):
    """
    Представлення для відображення списку улюблених товарів.
    """

    template_name = "wishlist/wishlist.html"
    context_object_name = "products"

    crumbs = [
        ("Всі товари", reverse_lazy("goods:catalog")),
        ("Бажані товари", reverse_lazy("wishlist:favorite")),
    ]

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
