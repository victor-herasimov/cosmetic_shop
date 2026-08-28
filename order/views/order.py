"""
Модуль представлень (Views) для обробки процесів замовлень.

Містить класи, які відповідають за відображення інтерфейсу оформлення
замовлення.
"""

from typing import Any

from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import FormView
from view_breadcrumbs import BaseBreadcrumbMixin

from order.forms import CreateOrderForm
from order.models.order import Order
from order.services import DeliveryMethodService, PaymentMethodService, OrderService


class OrderView(BaseBreadcrumbMixin, FormView):
    """
    Представлення для відображення сторінки оформлення замовлення (Checkout).

    Завантажує та рендерить сторінку з формою, де користувач вказує
    свої персональні дані.
    """

    form_class = CreateOrderForm

    template_name = "order/checkout.html"

    crumbs = [
        ("Оформити", ""),
    ]

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("HX-Request"):
            return ["order/includes/_form_create.html"]
        return [self.template_name]

    def get_initial(self) -> dict[str, Any]:
        """Встановлюємо початкові дані для форми, а саме метод доставки."""
        initial: dict[str, Any] = super().get_initial()
        initial["delivery_method"] = DeliveryMethodService.get_active_first()
        initial["payment_method"] = PaymentMethodService.get_active_first()

        return initial

    def form_valid(self, form) -> HttpResponse:
        """Якщо форма валідна то зберігає замовлення і редіректить на сторінку подяки."""
        order: Order = OrderService(self.request, form.cleaned_data).create_order()

        response: HttpResponse = HttpResponse(status=200)
        response["HX-Redirect"] = reverse("checkout:order_success", args=[order.id])
        return response
