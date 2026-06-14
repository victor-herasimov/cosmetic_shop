from typing import Any

from django.core.paginator import Page, Paginator
from django.http import Http404
from django.views.generic import ListView
from django.conf import settings

from goods.models.category import Category
from goods.services import CategoryService, ProductService
from goods.forms import ProductSortForm


class CatalogView(ListView):
    """
    Представлення для відображення каталогу товарів.
    """

    # template_name = "goods/catalog.html"
    context_object_name = "products"
    paginate_by = settings.ITEMS_PER_PAGE

    SORT_MAPPING = {
        "default": "-updated",
        "name_asc": "title",
        "name_desc": "-title",
        "price_asc": "price",
        "price_desc": "-price",
        "bestsellers_asc": "-is_bestseller",
        "bestsellers_desc": "is_bestseller",
    }

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("HX-Request"):
            return ["goods/includes/products.html"]
        return ["goods/catalog.html"]

    def _get_active_category(self, slug: str) -> Category:
        """
        При першому виклику отримує категорія з бази даних по слагуі кешує її в пам`ять.
        При на ступних викликах в межах одного http запиту повертає закешоване значення.
        """
        if not hasattr(self, "_data_by_slug_cache"):
            self._data_by_slug_cache: dict[str, Category] = {}

        if slug in self._data_by_slug_cache:
            return self._data_by_slug_cache[slug]

        try:
            result: Category = CategoryService().get_category_by_slug(slug)
            self._data_by_slug_cache[slug] = result
            return result
        except Category.DoesNotExist as exc:
            raise Http404("Категорію не знайдено") from exc

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

        cat_slug: str | None = self.request.GET.get("cat")
        if not cat_slug:
            return ProductService().get_all(order=order_field)

        active_category = self._get_active_category(cat_slug)

        return ProductService().get_products_by_category(
            active_category, order=order_field
        )

    def get_context_data(self, **kwargs):
        """
        Повертає словник контексту для рендерингу шаблону.
        Доповнює базовий контекст наступними даними даними: category_with_count_products,
        які будуть доступні в HTML-шаблоні.
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["category_with_count_products"] = (
            CategoryService().get_all_with_count_products()
        )
        context["active_category"] = (
            self._get_active_category(self.request.GET.get("cat"))
            if self.request.GET.get("cat")
            else None
        )
        context["total_products"] = ProductService().get_products_count()
        paginator: Paginator = context["paginator"]
        page_obj: Page = context["page_obj"]
        context["elided_page_range"] = paginator.get_elided_page_range(
            number=page_obj.number, on_each_side=1, on_ends=1
        )
        context["order_form"] = self.form
        return context
