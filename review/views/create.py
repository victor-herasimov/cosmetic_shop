import time
from typing import Any

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView
from django.core.paginator import Page, Paginator

from goods.models.product import Product
from goods.services.product import ProductService
from mixins import HTMXLoginRequiredMixin, OnlyHtmxMixin
from review.forms import ReviewCreateForm
from review.models import Review
from review.services import ReviewService


class ReviewCreateView(HTMXLoginRequiredMixin, OnlyHtmxMixin, FormView):
    form_class = ReviewCreateForm
    paginate_by = 1

    show_form_template = "review/includes/_show_form_template.html"
    hide_form_template = "review/includes/_hide_form_template.html"
    valid_template = "review/includes/_valid_template.html"
    invalid_template = "review/includes/_invalid_template.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        response: HttpResponse = super().get(request, *args, **kwargs)

        return response

    def get_template_names(self) -> list[str]:
        action: str = self.request.GET.get("action", "show")

        if self.request.method == "GET" and action == "show":
            return [self.show_form_template]

        if self.request.method == "GET" and action == "hide":
            return [self.hide_form_template]

        return super().get_template_names()

    def get_initial(self) -> dict[str, Any]:
        review: Review | None = ReviewService.get(
            self.request.user, self.kwargs.get("product_id")
        )

        if review:
            return {"rating": review.rating, "text": review.text}

        return {"rating": 1}

    def form_valid(self, form) -> HttpResponse:
        product_id: int = self.kwargs.get("product_id")

        _, created = ReviewService.update_or_create(
            self.request.user, product_id, form.cleaned_data
        )

        product: Product = ProductService(self.request).get_by_id(product_id)

        paginator: Paginator = Paginator(product.reviews.all(), self.paginate_by)
        review_page_obj: Page = paginator.get_page(1)

        toast_text: str = (
            "Ви успішно створили новий відгук"
            if created
            else "Ваш відгук успішно оновлено!"
        )

        context: dict[str, Any] = {
            "product": product,
            "review_page_obj": review_page_obj,
            "action": "update",
            "time": int(time.time() * 1000),
            "toast_text": toast_text,
        }
        return render(self.request, self.valid_template, context=context)

    def form_invalid(self, form) -> HttpResponse:
        """
        Обробляє випадок, коли форма містить помилки валідації.

        Повторно рендерить форму редагування, передаючи до контексту
        об'єкт форми з помилками для відображення їх користувачеві.
        Відображає тост з помилками
        """

        context: dict[str, Any] = {
            "form": form,
            "product_id": self.kwargs.get("product_id"),
            "action": "review-error",
            "time": int(time.time() * 1000),
            "toast_text": "Сталася помилка",
        }
        response = render(self.request, self.invalid_template, context=context)
        response["HX-Retarget"] = "#reviewFormContainer"
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_id"] = self.kwargs.get("product_id")

        return context
