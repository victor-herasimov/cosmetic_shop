"""
Модуль для обробки перенаправлень, пов'язаних із розділом обраного (wishlist).
"""

from django.shortcuts import redirect
from django.views.generic import View
from django.http import HttpResponse
from django.urls import reverse

from mixins.htmx_login_required_mixin import HTMXLoginRequiredMixin
from mixins.only_htmx_mixin import OnlyHtmxMixin


class FavoriteRedirectView(HTMXLoginRequiredMixin, OnlyHtmxMixin, View):
    """
    Представлення для HTMX-перенаправлення користувача на сторінку обраного.

    Працює виключно з HTMX-запитами та вимагає авторизації.
    """

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Обробляє GET-запит та повертає відповідь із заголовком 'HX-Redirect'.
        """
        # Якщо це HTMX запит — відправляємо заголовок для редіректу
        if request.headers.get("HX-Request"):
            response = HttpResponse()
            response["HX-Redirect"] = reverse("wishlist:favorite")
            return response

        # Якщо це звичайний запит — робимо стандартний Django redirect
        return redirect("wishlist:favorite")
