"""
Модуль для керування процесом скидання пароля користувачів.

Містить класи відображення (views), які інтегруються з HTMX для забезпечення
динамічного та безшовного UX/UI без повного перезавантаження сторінок.
"""

from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from django.shortcuts import render

from account.services import UserService
from account.forms import PasswordResetForm
from mixins import OnlyHtmxMixin


class PasswordResetView(OnlyHtmxMixin, View):
    """
    Відображення (View) для обробки запитів на скидання пароля користувача.

    Працює виключно через HTMX (завдяки OnlyHtmxMixin). Повертає HTML-фрагменти
    модального вікна, форми або повідомлення про успішне відправлення листа.
    """

    template_name_get: str = "includes/_password_reset_modal.html"
    template_name_post: str = "account/includes/_success_reset_password.html"
    template_name_email_text: str = "account/password_reset_email.txt"
    template_name_email_html: str = "account/password_reset_email.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Обробляє GET-запит. Повертає HTML-структуру модального вікна з порожньою формою.

        Додає HTMX-заголовок 'HX-Trigger-After-Swap' для ініціалізації
        відкриття модального вікна на стороні фронтенду після вставки HTML.
        """
        response: HttpResponse = render(
            request,
            self.template_name_get,
            {"password_reset_form": PasswordResetForm()},
        )
        response["HX-Trigger-After-Swap"] = "showPasswordResetModal"
        return response

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Обробляє POST-запит (відправку форми).

        Якщо форма валідна:
            Викликає сервіс для надсилання email та повертає шаблон успіху.
        Якщо форма невалідна:
            Повертає шаблон форми з помилками та перевизначає ціль вставки
            через HTMX-заголовок 'HX-Retarget' для локального оновлення форми.
        """
        form: PasswordResetForm = PasswordResetForm(data=request.POST)

        if form.is_valid():
            # send message
            UserService.send_password_reset_email(
                request=request,
                user_email=form.cleaned_data["email"],
                template_name_email_text=self.template_name_email_text,
                template_name_email_html=self.template_name_email_html,
            )
            return render(
                request,
                self.template_name_post,
                {},
            )
        else:
            response: HttpResponse = render(
                request, "account/includes/_password_reset_form.html", {"form": form}
            )
            response["HX-Retarget"] = "#passwordResetForm"

            return response
