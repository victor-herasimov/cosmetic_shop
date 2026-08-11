"""
Модуль для відображення сторінок з відгуками про товари.

Цей модуль містить представлення (Views) для пагінованого завантаження
та відображення відгуків, пов'язаних із конкретними продуктами.
"""

from typing import Any

from django.db.models import QuerySet
from django.http import Http404, HttpRequest
from django.views.generic import ListView

from goods.models.product import Product
from goods.services import ProductService
from review.models import Review


class GetReviewPageView(ListView):
    """Представлення для пагінованого відображення відгуків продукту.

    Отримує ідентифікатор продукту з URL-аргументів, завантажує відповідний
    продукт через `ProductService` та повертає сторінку з його відгуками.

    Attributes:
        paginate_by (int): Кількість відгуків на одній сторінці пагінації.
        template_name (str): Шлях до HTML-шаблону відображення відгуків.
        context_object_name (str): Назва змінної списку відгуків у контексті шаблону.
        product (Product): Екземпляр продукту, отриманий у методі `setup`.
    """

    paginate_by = 1
    template_name = "review/includes/_paginate_template.html"

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        """Ініціалізація продукту один раз перед викликом інших методів."""
        super().setup(request, *args, **kwargs)

        product_id: int | None = self.kwargs.get("product_id")
        if not product_id:
            raise Http404("Не переданий ідентифікатор продукта")

        product_service = ProductService(request)
        try:
            self.product: Product = product_service.get_by_id(product_id=product_id)
        except Product.DoesNotExist as e:
            raise Http404(f"Продукт з id {product_id} не знайдено") from e

    def get_queryset(self) -> QuerySet[Review]:
        """Формує та повертає QuerySet відгуків для обраного продукту.
        Returns:
            QuerySet[Review]: Набір відгуків, що належать даному продукту.
        """
        return self.product.reviews.all()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Розширює контекст шаблону додатковими даними.

        Додає об'єкт `product` та копію об'єкта сторінки пагінації під
        ключем `review_page_obj` для зручності використання в AJAX/partial шаблонах.
        """
        context = super().get_context_data(**kwargs)
        context["product"] = self.product
        context["review_page_obj"] = context["page_obj"]

        return context
