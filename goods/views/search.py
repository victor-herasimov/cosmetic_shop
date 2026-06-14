from typing import Any

from django.conf import settings
from django.core.paginator import Page, Paginator
from django.views.generic import ListView

from goods.services import ProductService
from goods.forms import ProductSortForm


class SearchView(ListView):
    """
    Представлення для відображення пошуку.
    """

    context_object_name = "products"
    paginate_by = settings.ITEMS_PER_PAGE

    SORT_MAPPING = {
        "default": "-updated",
        "name_asc": "title",
        "name_desc": "-title",
        "price_asc": "price",
        "price_desc": "-price",
        "bestsellers_asc": "is_bestseller",
        "bestsellers_desc": "-is_bestseller",
    }

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("HX-Request"):
            return ["goods/includes/search_products.html"]
        return ["goods/search.html"]

    def get_queryset(self):
        """
        Повертає відфільтрований список товарів для каталогу.
        """
        self.form = ProductSortForm(self.request.GET)

        if self.form.is_valid():
            sort_by = self.form.cleaned_data.get("sort")
            order_field = self.SORT_MAPPING.get(sort_by, "-updated")
        else:
            order_field = "-updated"

        search_text: str | None = self.request.GET.get("search", "")
        return ProductService().search(search_text, order=order_field)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Повертає словник контексту для рендерингу шаблону.
        Доповнює базовий контекст наступними даними даними: order_form, elided_page_range,
        які будуть доступні в HTML-шаблоні.
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["order_form"] = self.form
        paginator: Paginator = context["paginator"]
        page_obj: Page = context["page_obj"]
        context["elided_page_range"] = paginator.get_elided_page_range(
            number=page_obj.number, on_each_side=1, on_ends=1
        )
        return context
