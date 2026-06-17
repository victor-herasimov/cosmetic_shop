from typing import Any
from django.http import Http404, HttpRequest, HttpResponseBadRequest
from django.views.generic import View
from django.shortcuts import render

from cart.cart import Cart
from cart.forms import CartAddForm
from goods.models.product import Product
from goods.services.product import ProductService


class CartUpdateView(View):
    """
    Оновлення кількості продуктів в кошику.
    """

    template_name = "cart/includes/_cart_update_item.html"

    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Повертає оновлену верстку картки продукту в кошику.
        """
        cart: Cart = Cart(request)
        form: CartAddForm = CartAddForm(request.POST)

        if form.is_valid():
            cd: dict[str, Any] = form.cleaned_data
            try:
                product: Product = ProductService().get_by_id(cd["product_id"])
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
                template_name=self.template_name,
                context={
                    "cart": cart,
                    "cart_item": cart.get_item_by_product(product),
                },
            )
        else:
            return HttpResponseBadRequest("Форма не валідна.")
