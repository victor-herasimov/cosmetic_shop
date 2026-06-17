from typing import Any
from django.http import Http404, HttpRequest, HttpResponseBadRequest, HttpResponse
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

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.delete(request, args, kwargs)

    def delete(self, request: HttpRequest, *args, **kwargs):
        "Видаляє продукт з кошика за його ID переданим в тілі запиту."

        cart: Cart = Cart(request)
        form: CartRemoveForm = CartRemoveForm(request.POST)

        if form.is_valid():
            cd: dict[str, Any] = form.cleaned_data
            try:
                product: Product = ProductService().get_by_id(cd["product_id"])
            except Product.DoesNotExist as exc:
                raise Http404("Товару не знайдено") from exc

            cart.remove(product=product)

            template_name: str = "cart/includes/_cart_remove_item.html"
            context = {
                "cart": cart,
                "toast": True,
                "toast_text": f"{product.title} видалено з кошика.",
                "update_cart_count": True,
            }
            if not cart:
                template_name = "cart/includes/cart_body.html"
                context["footer_oob"] = True

            return render(request, template_name, context)

        else:

            return HttpResponseBadRequest("Форма не валідна.")
