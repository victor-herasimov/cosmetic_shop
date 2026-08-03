"""
Модуль для керування видаленням облікових записів користувачів.

Цей модуль містить представлення (view), яке дозволяє авторизованим користувачам
повністю видалити свій профіль із системи. Процес інтегрований з HTMX:
після успішного видалення облікового запису користувач розлогінюється, а його
браузер безшовно перенаправляється на головну сторінку.
"""

from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import logout

from account.models import User as CustomUser
from mixins import HTMXLoginRequiredMixin, OnlyHtmxMixin


class DeleteUserView(HTMXLoginRequiredMixin, OnlyHtmxMixin, View):
    """
    Представлення для видалення профілю поточного користувача.

    Вимагає обов'язкової авторизації (`LoginRequiredMixin`). Обробляє лише
    POST-запити для забезпечення безпеки (запобігання випадковому видаленню
    через GET-запити чи пошукових роботів).
    """

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Обробляє POST-запит на видалення облікового запису.

        Виконує операцію видалення користувача з бази даних та завершення
        сеансу (logout) в межах однієї атомарної транзакції. Після цього
        повертає відповідь із заголовком 'HX-Redirect' для HTMX.
        """
        user: CustomUser = request.user
        with transaction.atomic():
            user.delete()
            logout(request)

        response: HttpResponse = HttpResponse(status=200)
        response["HX-Redirect"] = reverse("main:index")
        return response
