"""
Модуль представлень (Views) для сторінки успішного замовлення.

Містить клас, який відповідає за відображення інтерфейсу подяки за
замовлення.
"""

from typing import Any

from django.views.generic import TemplateView


class OrderSuccessView(TemplateView):
    """
    Представлення для відображення сторінки успішного оформлення замовлення (Success).
    """

    template_name = "order/success.html"

    def get_context_data(self, **kwargs):
        """
        Додає до контексту ID замовлення order_id, яке бере з параметрів щляху
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["order_id"] = self.kwargs.get("order_id")

        return context
