"""
Модуль для обробки видалення відгуків про товари.

Забезпечує контролер (View) для видалення відгуків користувачами
через HTMX-запити з поверненням відповідних шаблонів та заголовків.
"""

import time
from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Page, Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from goods.models import Product
from goods.services import ProductService
from mixins.htmx_login_required_mixin import HTMXLoginRequiredMixin
from mixins.only_htmx_mixin import OnlyHtmxMixin
from review.services import ReviewService


class ReviewDeleteView(HTMXLoginRequiredMixin, OnlyHtmxMixin, View):
    """
    View-клас для видалення відгуків про товари через HTMX-запити.
    """

    valid_template = "review/includes/_valid_template.html"
    invalid_template = "review/includes/_toast.html"
    paginate_by = 1

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Обробляє POST-запит на видалення відгуку.

        """
        review_id: int = self.kwargs.get("review_id")

        is_deleted: bool = ReviewService.delete(review_id=review_id, user=request.user)

        context: dict[str, Any] = {
            "action": "delete",
            "time": int(time.time() * 1000),
        }

        template = self.invalid_template
        toast_text = "Щось пішло не так"

        if is_deleted:
            product_id = request.GET.get("product")
            if product_id:
                try:
                    product: Product = ProductService(request).get_by_id(product_id)

                    paginator: Paginator = Paginator(
                        product.reviews.all(), self.paginate_by
                    )
                    review_page_obj: Page = paginator.get_page(1)

                    template = self.valid_template
                    toast_text: str = "Ви успішно видалили відгук"
                    context.update(
                        {
                            "product": product,
                            "review_page_obj": review_page_obj,
                        }
                    )

                except (ObjectDoesNotExist, ValueError):
                    pass

        context["toast_text"] = toast_text

        response: HttpResponse = render(self.request, template, context=context)

        response["HX-Trigger"] = "closeDeleteReviewModal"
        response["HX-Reswap"] = "none"

        return response
