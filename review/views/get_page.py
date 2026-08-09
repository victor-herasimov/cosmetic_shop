from django.db.models import QuerySet
from django.http import Http404
from django.views.generic import ListView

from goods.models.product import Product
from goods.services import ProductService
from review.models import Review


class GetReviewPageView(ListView):
    paginate_by = 1
    template_name = "review/includes/_paginate_template.html"

    def get_queryset(self) -> QuerySet[Review]:
        product_id: int = self.kwargs.get("product_id")
        product_service: ProductService = ProductService(self.request)

        if not product_id:
            raise Http404("Не переданий ідентифікатор продукта")

        try:
            self.product: Product = product_service.get_by_id(product_id=product_id)
        except Product.DoesNotExist as e:
            raise Http404(f"Продукт з {product_id} не знайдено") from e

        return self.product.reviews.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = self.product
        context["review_page_obj"] = context["page_obj"]

        return context
