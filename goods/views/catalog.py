from typing import Any

from django.http import Http404
from django.views.generic import ListView
from goods.models.category import Category
from goods.services import CategoryService, ProductService


class CatalogView(ListView):
    """
    Представлення для відображення каталогу товарів.
    """

    template_name = "goods/catalog.html"
    context_object_name = "products"

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
        cat_slug: str | None = self.request.GET.get("cat")
        if not cat_slug:
            return ProductService().get_all()

        active_category = self._get_active_category(cat_slug)

        return ProductService().get_products_by_category(active_category)

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
        return context
