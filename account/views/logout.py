"""
Модуль для керування логауту користувачів у системі.

Містить представлення (Views) для безпечного виходу
та адміністрування сесій користувачів з інтеграцією HTMX.
"""

import time
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout as user_logout
from django.shortcuts import render

from mixins import OnlyHtmxMixin
from account.forms import EmailOrPhoneLoginForm, UserRegistrationForm


class LogoutView(LoginRequiredMixin, OnlyHtmxMixin, View):
    """
    Представлення для виходу користувача з системи через HTMX-запит.

    Забезпечує безпечне завершення сесії авторизованого користувача,
    зберігаючи при цьому вміст його кошика покупок для анонімної сесії.
    Доступно лише для автентифікованих користувачів та через HTMX.
    """

    template_name = "account/includes/_success_logout.html"

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Обробляє POST-запит на вихід з облікового запису.

        Видаляє дані сесії користувача, перевипускає анонімну сесію,
        переносить у неї кошик покупок (`cart`), рендерить форму логіну
        та ініціює клієнтську подію 'userLoggedOut' через HTMX.

        Args:
            request (HttpRequest): Об'єкт HTTP-запиту Django.
            *args (Any): Додаткові позиційні аргументи.
            **kwargs (Any): Додаткові іменовані аргументи.

        Returns:
            HttpResponse: Частковий HTML-шаблон успішного виходу з форми входу
            та HTMX-заголовком `HX-Trigger`.
        """
        cart: dict[str, Any] = request.session.get("cart", {})
        user_logout(request)
        if cart:
            request.session["cart"] = cart

        request.session.modified = True

        response: HttpResponse = render(
            request,
            self.template_name,
            {
                "login_form": EmailOrPhoneLoginForm(),
                "logout_form": UserRegistrationForm(),
                "action": "logout",
                "time": int(time.time() * 1000),
                "toast_text": "Ви успішно вийшли з особистого кабінету",
            },
        )
        response["HX-Trigger"] = "userLoggedOut"

        return response
