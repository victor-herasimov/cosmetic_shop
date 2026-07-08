"""
Модуль контекстних процесорів для автентифікації користувачів.

Цей модуль надає глобальні змінні для шаблонів Django, які пов'язані з процесом
входу та реєстрації. Використовується для ініціалізації початкового стану форм
(наприклад, у модальних вікнах або шапці сайту) перед їхньою подальшою обробкою
асинхронними HTMX-запитами.
"""

from django.http import HttpRequest

from .forms import EmailOrPhoneLoginForm, UserRegistrationForm


def auth_forms(request: HttpRequest) -> dict[str, EmailOrPhoneLoginForm]:
    """
    Контекстний процесор для надання початкової форми автентифікації всім шаблонам.

    Робить порожній екземпляр форми `EmailOrPhoneLoginForm` доступним у будь-якому
    HTML-шаблоні через змінну `{{ login_form }}`.

    Оскільки в проєкті використовується HTMX, цей процесор виконує роль ініціалізатора
    стану для первинного GET-запиту. У випадку помилок валідації під час POST-запиту,
    відповідна View поверне відрендерений partial-шаблон форми з помилками, який замінить
    поточний елемент у DOM без перезавантаження сторінки.

    Args:
        request (HttpRequest): Об'єкт поточного HTTP-запиту.

    Returns:
        dict[str, EmailOrPhoneLoginForm]: Словник із формою входу для початкового рендерингу.
    """
    return {
        "login_form": EmailOrPhoneLoginForm(),
        "register_form": UserRegistrationForm(),
    }
