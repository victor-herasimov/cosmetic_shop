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

    def get_object(self, queryset=...):
        """
        Повертає об`єкт Продукта, якщо такий існує.
        """
        slug: str = self.kwargs.get(self.slug_url_kwarg)
        try:
            obj: Product = ProductService().get_by_slug(slug)
        except Product.DoesNotExist as exc:
            raise Http404(f"Продукт з слагом {slug} не знайдено") from exc
        return obj

    def get_context_data(self, **kwargs):
        """
        Повертає словник контексту для рендерингу шаблону.
        Доповнює базовий контекст наступними даними даними: similar_products,
        які будуть доступні в HTML-шаблоні.
        """
        context = super().get_context_data(**kwargs)
        context["similar_products"] = ProductService().get_similar_products(
            product_slug=self.kwargs.get(self.slug_url_kwarg)
        )
        return context
