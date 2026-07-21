from typing import Any
from django.http import (
    Http404,
    HttpRequest,
    HttpResponseBadRequest,
    HttpResponse,
)
from django.urls import reverse
from django.views.generic import View
from django.shortcuts import render

from cart.cart import Cart
from cart.forms import CartRemoveForm
from goods.models.product import Product
from goods.services.product import ProductService
from mixins.only_htmx_mixin import OnlyHtmxMixin


class CartRemoveView(OnlyHtmxMixin, View):
    """
    Представлення для видалення продукту з кошика.
    """

    checkout_path: str = "checkout"

    def _render_cart_in_checkout_page(
        self, request: HttpRequest, cart: Cart, product: Product
    ) -> HttpResponse:
        """
        Рендер елементів кошика на сторінці замовлення
        """
        if not cart:
            response: HttpResponse = HttpResponse(status=200)
            response["HX-Redirect"] = reverse("goods:catalog")
            return response

        template_name: str = "order/includes/_order_remove_item.html"
        context: dict[str, Any] = {
            "cart": cart,
            "toast": True,
            "toast_text": f"{product.title} видалено з кошика.",
        }

        return render(request, template_name, context)

    def _render_cart_in_cart_modal(
        self, request: HttpRequest, cart: Cart, product: Product
    ) -> HttpResponse:
        """
        Рендер елементів кошика в модальному вікні кошика
        """
        template_name: str = "cart/includes/_cart_remove_item.html"
        context: dict[str, Any] = {
            "cart": cart,
            "toast": True,
            "toast_text": f"{product.title} видалено з кошика.",
            "update_cart_count": True,
        }
        if not cart:
            template_name = "cart/includes/cart_body.html"
            context["footer_oob"] = True

        return render(request, template_name, context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Видаляє продукт з кошика за його ID переданим в тілі запиту.
        """
        cart: Cart = Cart(request)
        form: CartRemoveForm = CartRemoveForm(request.POST)
        current_url: str = request.headers.get("HX_Current-Url", "")

        if not form.is_valid():
            return HttpResponseBadRequest("Форма не валідна.")

        cd: dict[str, Any] = form.cleaned_data
        try:
            product: Product = ProductService(request.GET).get_by_id(cd["product_id"])
        except Product.DoesNotExist as exc:
            raise Http404("Товару не знайдено") from exc

        cart.remove(product=product)

        if self.checkout_path in current_url:
            # Рендер елементів кошика на сторінці замовлення
            return self._render_cart_in_checkout_page(request, cart, product)
        # Рендер елементів кошика в модальному вікні кошика
        return self._render_cart_in_cart_modal(request, cart, product)
