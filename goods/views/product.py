from typing import Any

from django.core.paginator import Page, Paginator
from django.http import Http404
from django.views.generic import DetailView
from goods.models.product import Product
from goods.services import ProductService


class ProductDetailView(DetailView):
    """
    Представлення для відображення детальної інформації про товар.
    """

    template_name = "goods/product.html"
    context_object_name = "product"
    slug_url_kwarg = "slug"
    paginate_by: int = 1

    def get_object(self, queryset=None) -> Product:
        """
        Повертає об`єкт Продукта, якщо такий існує.
        """
        slug: str = self.kwargs.get(self.slug_url_kwarg)
        try:
            obj: Product = ProductService(self.request).get_by_slug(slug)
        except Product.DoesNotExist as exc:
            raise Http404(f"Продукт з слагом {slug} не знайдено") from exc
        return obj

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Повертає словник контексту для рендерингу шаблону.
        Доповнює базовий контекст наступними даними даними: similar_products,
        які будуть доступні в HTML-шаблоні.
        """
        context = super().get_context_data(**kwargs)
        context["similar_products"] = ProductService(self.request).get_similar_products(
            product=self.object
        )

        product: Product = context[self.context_object_name]
        paginator: Paginator = Paginator(product.reviews.all(), self.paginate_by)
        review_page_obj: Page = paginator.get_page(1)
        context["review_page_obj"] = review_page_obj
        context["meta"] = self.object.as_meta(self.request)

        return context
