"""
Модуль представлень (Views) для обробки процесів замовлень.

Містить класи, які відповідають за відображення інтерфейсу оформлення
замовлення.
"""

from typing import Any

from django.views.generic import FormView
from order.forms import CreateOrderForm
from order.services import DeliveryMethodService, PaymentMethodService


class OrderView(FormView):
    """
    Представлення для відображення сторінки оформлення замовлення (Checkout).

    Завантажує та рендерить сторінку з формою, де користувач вказує
    свої персональні дані.
    """

    form_class = CreateOrderForm

    template_name = "order/checkout.html"

    def get_initial(self) -> dict[str, Any]:
        """Встановлюємо початкові дані для форми, а саме метод доставки."""
        initial: dict[str, Any] = super().get_initial()
        initial["delivery_method"] = DeliveryMethodService.get_active_first()
        initial["payment_method"] = PaymentMethodService.get_active_first()

        return initial
