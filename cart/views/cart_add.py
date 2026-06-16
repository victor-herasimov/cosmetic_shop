from typing import Any
from django.http import Http404, HttpRequest, HttpResponseBadRequest
from django.views.generic import View
from django.shortcuts import render

from cart.cart import Cart
from cart.forms import CartAddForm
from goods.models.product import Product
from goods.services.product import ProductService


class CartAddView(View):
    """
    Представлення для додавання продукту в кошик.
    """

    template_name = "includes/cart_body.html"

    def post(self, request: HttpRequest, *args, **kwargs):
        cart: Cart = Cart(request)

        form: CartAddForm = CartAddForm(request.POST)

        if form.is_valid():
            cd: dict[str, Any] = form.cleaned_data
            try:
                product: Product = ProductService().get_by_id(cd["product_id"])
            except Product.DoesNotExist as exc:
                raise Http404("Товару не знайдено") from exc
            cart.add(
                product=product,
                quantity=cd["quantity"],
                override_quantity=cd["override"],
            )
            toast_text: str = f"{product.title} додано в кошик."
            return render(
                request,
                template_name=self.template_name,
                context={
                    "cart": cart,
                    "toast": True,
                    "toast_text": toast_text,
                    "footer": True,
                    "product": product,
                    "htmx_query": True,
                },
            )
        else:
            HttpResponseBadRequest("Форма не валідна.")
