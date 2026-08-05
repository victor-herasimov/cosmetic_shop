"""
Модуль для обробки HTMX-запитів, пов'язаних із списком обраного (wishlist).

Містить представлення для додавання та видалення товарів з обраного.
"""

import time

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View

from goods.models.product import Product
from goods.services.product import ProductService
from mixins.htmx_login_required_mixin import HTMXLoginRequiredMixin
from mixins.only_htmx_mixin import OnlyHtmxMixin
from wishlist.services import FavoriteService


class ToggleFavoriteView(OnlyHtmxMixin, HTMXLoginRequiredMixin, View):
    """
    Представлення для перемикання стану товару в списку обраного (додавання/видалення).

    Працює виключно з HTMX-запитами та вимагає аутентифікації користувача.
    """

    template_name = "wishlist/toggle.html"

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Обробляє POST-запит для додавання або видалення товару з обраного.
        """
        favorite_service: FavoriteService = FavoriteService(request)
        product_id: int | None = self.kwargs.get("product_id")

        if not product_id:
            message: str = "Не вдалося виконати дію"
            return render(
                request,
                self.template_name,
                context={
                    "error": True,
                    "toast_text": message,
                    "action": "error",
                    "time": int(time.time() * 1000),
                },
            )
        is_favorite: bool = favorite_service.toggle(product_id)
        has_favorite: bool = favorite_service.has_favorite()
        from_detail: bool = request.POST.get("from_detail") == "true"
        message: str = (
            "Товар успішно добавлено до улюблених"
            if is_favorite
            else "Товар успішно видалено з улюблених"
        )

        product: Product = ProductService(request).get_by_id(product_id)

        return render(
            request,
            self.template_name,
            context={
                "error": False,
                "toast_text": message,
                "from_detail": from_detail,
                "action": "success",
                "time": int(time.time() * 1000),
                "user_has_favorite": has_favorite,
                "product": product,
            },
        )
