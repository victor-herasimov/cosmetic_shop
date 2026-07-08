"""Модуль контролера (Views) для реєстрації користувачів.

Цей модуль містить класи для обробки запитів реєстрації, адаптовані
для безшовної роботи з бібліотекою HTMX (асинхронні HTML-відповіді).
"""

import time
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import login as user_login, get_user_model
from django.contrib.auth.models import AbstractUser

from account.forms import UserRegistrationForm
from account.services import UserService

User: type[AbstractUser] = get_user_model()


class RegisterView(View):
    """
    Контролер для реєстрації нових користувачів.

    Обробляє POST-запити від форми реєстрації. Заточений під HTMX:
    повертає частковий HTML (partial) замість повносторінкового рендеру.
    """

    template_name = "account/includes/register_form.html"

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Обробляє відправку форми реєстрації.

        У разі успішної валідації: створює користувача через UserService,
        автоматично логінить його та повертає шаблон успіху із заголовком
        `HX-Trigger` для фронтенду.
        У разі помилки: повертає форму з помилками та вказує селектор для
        перенаправлення контенту через `HX-Retarget`.
        """

        form: UserRegistrationForm = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            user: AbstractUser = UserService.create(data=form.cleaned_data)
            user_login(request, user)
            response: HttpResponse = render(
                request,
                "account/includes/_success_auth.html",
                {
                    "action": "login",
                    "time": int(time.time() * 1000),
                    "toast_text": f"Ви успішно зареєструвалися і увійшли як {user.first_name} {user.last_name}",
                },
            )
            response["HX-Trigger"] = "userLoggedIn"
            return response
        else:
            response: HttpResponse = render(request, self.template_name, {"form": form})
            response["HX-Retarget"] = "#registerForm"

            return response
