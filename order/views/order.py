"""
Модуль представлень (Views) для обробки процесів замовлень.

Містить класи, які відповідають за відображення інтерфейсу оформлення
замовлення.
"""

from django.views.generic import FormView
from order.forms import CreateOrderForm


class OrderView(FormView):
    """
    Представлення для відображення сторінки оформлення замовлення (Checkout).

    Завантажує та рендерить сторінку з формою, де користувач вказує
    свої персональні дані.
    """

    form_class = CreateOrderForm

    template_name = "order/checkout.html"
