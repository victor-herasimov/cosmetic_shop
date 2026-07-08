"""
Модуль автентифікації користувачів для додатка account.

Містить класи та логіку для обробки запитів, пов'язаних із входом користувачів.
Всі представлення (Views) у цьому модулі
оптимізовані для роботи з HTMX-запитами, мінімізуючи повне перезавантаження сторінок
та забезпечуючи динамічну взаємодію з інтерфейсом (модальними вікнами, тостами тощо).
"""

import time
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import login as user_login

from account.forms import EmailOrPhoneLoginForm
from account.models import User


class LoginView(View):
    """
    Представлення (View) для автентифікації користувачів через HTMX.

    Обробляє логіку входу за допомогою електронної пошти або номера телефону.
    Призначене суто для роботи з AJAX/HTMX запитами з модального вікна.
    GET-запити не підтримуються, оскільки форма попередньо вшита в DOM клієнта.
    """

    template_name = "account/includes/login_form.html"

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Обробка POST-запиту на автентифікацію користувача.

        Валідує форму `EmailOrPhoneLoginForm`.

        Якщо форма валідна:
            - Авторизує користувача в системі (оновлюючи сесію).
            - Повертає шаблон успіху `_success_auth.html`.
            - Додає HTMX-заголовок `HX-Trigger: userLoggedIn` для сповіщення фронтенду.

        Якщо форма невалідна:
            - Повертає шаблон форми з помилками валідації.
            - Додає HTMX-заголовок `HX-Retarget: #loginForm` для локальної заміни форми.

        Args:
            request (HttpRequest): Об'єкт поточного HTTP-запиту від Django.
            *args: Додаткові позиційні аргументи.
            **kwargs: Додаткові іменовані аргументи.

        Returns:
            HttpResponse: HTML-код відповіді з відповідними HTMX-заголовками.
        """
        form: EmailOrPhoneLoginForm = EmailOrPhoneLoginForm(request, data=request.POST)

        if form.is_valid():
            user: User = form.get_user()
            user_login(request, user)
            response: HttpResponse = render(
                request,
                "account/includes/_success_auth.html",
                {
                    "action": "login",
                    "time": int(time.time() * 1000),
                    "toast_text": "Вхід виконано успішно",
                },
            )
            response["HX-Trigger"] = "userLoggedIn"
            return response
        else:
            response: HttpResponse = render(request, self.template_name, {"form": form})
            response["HX-Retarget"] = "#loginForm"

            return response
