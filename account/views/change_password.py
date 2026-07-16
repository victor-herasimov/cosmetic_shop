"""
Модуль для керування обліковими записами користувачів.

Цей модуль містить клас (views), що дозволяє користувачам
редагувати інформацію свого профілю, зокрема змінювати пароль облікового запису.
Він інтегрується з Django-формами та підтримує динамічне повернення шаблонів
для безшовної роботи з AJAX/HTMX запитами.
"""

import time
from typing import Any

from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm


class ChangeUserPasswordView(LoginRequiredMixin, FormView):
    """
    Представлення для зміни пароля авторизованого користувача.

    Використовує `FormView` для обробки форми та `LoginRequiredMixin` для
    обмеження доступу неавторизованим користувачам. Підтримує динамічний
    вибір шаблону (перегляд інфо / редагування) залежно від GET-параметрів.
    """

    form_class = PasswordChangeForm
    template_name = "account/includes/_card_password_form.html"
    success_template_name = "account/includes/_change_password_success.html"
    info_template_name = "account/includes/_card_password_info.html"

    def get_form_kwargs(self) -> dict[str, Any]:
        """Встановлює користувача до форми, зберігаючи POST-дані."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_template_names(self) -> list[str]:
        """
        Визначає та повертає список шаблонів для рендерингу сторінки.

        Залежно від GET-параметра 'type' повертає або шаблон відображення
        інформації профілю ('info'), або шаблон форми редагування імені.

        Returns:
            list[str]: Список із назвою відповідного HTML-шаблону.
        """
        template_type: str = self.request.GET.get("type", "")
        if not template_type or template_type == "info":
            return [self.info_template_name]

        return [self.template_name]

    def form_valid(self, form) -> HttpResponse:
        """
        Обробляє успішно валідовану форму.

        Оновлює пароль поточного користувача в базі даних,
        актуалізує сесію авторизації, щоб уникнути розлогінювання,
        та повертає шаблон успішного збереження з контекстним повідомленням.
        """
        self.request.user.set_password(form.cleaned_data["new_password2"])
        self.request.user.save()
        update_session_auth_hash(self.request, self.request.user)
        return render(
            self.request,
            self.success_template_name,
            context={
                "action": "change-password",
                "time": int(time.time() * 1000),
                "toast_text": "Пароль змінено успішно!",
            },
        )

    def form_invalid(self, form) -> HttpResponse:
        """
        Обробляє випадок, коли форма містить помилки валідації.

        Повторно рендерить форму редагування, передаючи до контексту
        об'єкт форми з помилками для відображення їх користувачеві.
        """
        return render(self.request, self.template_name, context={"form": form})
