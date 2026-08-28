from typing import Any

from django.conf import settings
from django.core.paginator import Page, Paginator
from django.views.generic import ListView
from view_breadcrumbs import BaseBreadcrumbMixin

from account.forms import OrderFilterForm
from mixins import HTMXLoginRequiredMixin
from order.services import OrderService


class UserOrderList(BaseBreadcrumbMixin, HTMXLoginRequiredMixin, ListView):

    context_object_name = "orders"
    paginate_by = settings.ORDERS_PER_PAGE

    crumbs = [
        ("Мої замовлення", ""),
    ]

    def get_queryset(self):
        """
        Повертає відфільтрований список замовлент користувача.
        """

        order_filter_form: OrderFilterForm = OrderFilterForm(self.request.GET)
        status_filter: str | None = None
        if order_filter_form.is_valid():
            status_filter = order_filter_form.cleaned_data["filter"]

        if status_filter in ("all", ""):
            status_filter = None

        print(status_filter)
        order_service: OrderService = OrderService(self.request)
        return order_service.get_orders_for_authenticated_user(
            status_filter=status_filter
        )

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("HX-Request"):
            return ["account/includes/_ajax_orders.html"]
        return ["account/orders.html"]

    def get_context_data(self, **kwargs):
        """
        Повертає словник контексту для рендерингу шаблону.
        Будуємо багатовимірні фасети та додаємо їх у контекст.
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)

        paginator: Paginator = context["paginator"]
        page_obj: Page = context["page_obj"]
        context["elided_page_range"] = paginator.get_elided_page_range(
            number=page_obj.number, on_each_side=1, on_ends=1
        )
        context["status_form"] = OrderFilterForm(self.request.GET)

        return context
