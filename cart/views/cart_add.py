from typing import Any
from django.http import Http404, HttpRequest, HttpResponseBadRequest
from django.views.generic import View
from django.shortcuts import render

from cart.cart import Cart
from cart.forms import CartAddForm
from goods.models.product import Product
from goods.services.product import ProductService
from mixins.only_htmx_mixin import OnlyHtmxMixin


class CartAddView(OnlyHtmxMixin, View):
    """
    Представлення для додавання продукту в кошик.
    """

    template_name = "cart/includes/cart_body.html"

    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Обробляє POST-запит для додавання або оновлення кількості товару в кошику.
        Метод валідує отримані дані форми, перевіряє існування товару
        через сервісний шар і оновлює стан кошика в сесії. Результат
        повертається у вигляді HTML-фрагмента для HTMX-обов'язкових запитів.
        """
        cart: Cart = Cart(request)
        form: CartAddForm = CartAddForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                template_name=self.template_name,
                context={
                    "cart": cart,
                    "toast": True,
                    "toast_text": "При додаванні товару сталася помилка! Товар не було додано до кошика",
                },
            )

        cd: dict[str, Any] = form.cleaned_data
        try:
            product: Product = ProductService.get_by_id(cd["product_id"])
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
                "footer_oob": True,
                "update_cart_count": True,
            },
        )
