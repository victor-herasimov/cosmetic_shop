from typing import Any
from django.http import Http404, HttpRequest, HttpResponseBadRequest, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View
from django.shortcuts import render

from cart.cart import Cart
from cart.forms import CartRemoveForm
from goods.models.product import Product
from goods.services.product import ProductService


class CartRemoveView(View):
    """
    Представлення для видалення продукту з кошика.
    """

    template_name = "includes/cart_delete.html"

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
            toast_text: str = f"{product.title} видалено з кошика."
            if cart:
                return render(
                    request,
                    "includes/_cart_remove_item.html",
                    context={
                        "cart": cart,
                        "toast": True,
                        "toast_text": toast_text,
                        "htmx_query": True,
                    },
                )
            else:
                response = render(
                    request,
                    "includes/cart_body.html",
                    context={
                        "cart": cart,
                        "toast": True,
                        "toast_text": toast_text,
                        "footer": True,
                        "htmx_query": True,
                    },
                )
                # response["HX-Retarget"] = "#cartItems"
                # response["HX-Swap"] = "innerHTML"
                # print(" cart empty")
                return response
        else:
            HttpResponseBadRequest("Форма не валідна.")
