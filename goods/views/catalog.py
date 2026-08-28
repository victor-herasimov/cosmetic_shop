from typing import Any

from django.core.paginator import Page, Paginator
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.conf import settings
from view_breadcrumbs import BaseBreadcrumbMixin

from goods.services import ProductService
from goods.forms import ProductSortForm


class CatalogView(BaseBreadcrumbMixin, ListView):
    """
    Представлення для відображення каталогу товарів.
    """

    # template_name = "goods/catalog.html"
    context_object_name = "products"
    paginate_by = settings.ITEMS_PER_PAGE

    crumbs = [
        ("Всі товари", reverse_lazy("goods:catalog")),
    ]

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("HX-Request"):
            return ["goods/includes/_ajax_products.html"]
        return ["goods/catalog.html"]

    def get_queryset(self):
        """
        Повертає відфільтрований список товарів для каталогу.
        """
        self.product_service = ProductService(self.request)
        return self.product_service.get_filtered_products()

    def get_context_data(self, **kwargs):
        """
        Повертає словник контексту для рендерингу шаблону.
        Будуємо багатовимірні фасети та додаємо їх у контекст.
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)

        paginator: Paginator = context["paginator"]
        page_obj: Page = context["page_obj"]
        context["elided_page_range"] = paginator.get_elided_page_range(
            number=page_obj.number, on_each_side=1, on_ends=1
        )
        context["order_form"] = ProductSortForm(self.request.GET)
        context.update(self.product_service.get_facets())

        return context
