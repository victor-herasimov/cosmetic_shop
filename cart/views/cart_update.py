from typing import Any
from django.http import Http404, HttpRequest, HttpResponse
from django.views.generic import View
from django.shortcuts import render

from cart.cart import Cart
from cart.forms import CartAddForm
from goods.models.product import Product
from goods.services.product import ProductService
from mixins.only_htmx_mixin import OnlyHtmxMixin


class CartUpdateView(OnlyHtmxMixin, View):
    """
    Оновлення кількості продуктів в кошику.
    """

    checkout_path: str = "checkout"

    def _get_template_name(self) -> str:
        """
        Повертає шаблон в залежності від того з якої сторінки було надіслано запит.
        """
        current_url: str = self.request.headers.get("HX_Current-Url", "")

        if self.checkout_path in current_url:
            # Повернення шаблону кошика на сторінці оформлення замовлення
            return "order/includes/_order_update_item.html"

        # Повернення шаблону для модального вікна кошика
        return "cart/includes/_cart_update_item.html"

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Повертає оновлену верстку картки продукту в кошику.
        """
        cart: Cart = Cart(request)
        form: CartAddForm = CartAddForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                template_name="cart/includes/_toast.html",
                context={
                    "toast_text": "Сталася помилка. Не вдалося оновити кількість в кошику!"
                },
            )

        cd: dict[str, Any] = form.cleaned_data
        try:
            product: Product = ProductService.get_by_id(cd["product_id"])
        except Product.DoesNotExist as exc:
            raise Http404("Товару не знайдено") from exc

        action: str = cd["action"]
        quantity = cd["quantity"]

        if action:
            quantity = quantity + 1 if action == "add" else quantity - 1

        cart.add(
            product=product,
            quantity=quantity,
            override_quantity=cd["override"],
        )
        return render(
            request,
            template_name=self._get_template_name(),
            context={
                "cart": cart,
                "cart_item": cart.get_item_by_product(product),
            },
        )
