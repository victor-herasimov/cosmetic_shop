"""
Модуль конфігурації адміністративної панелі для кастомної моделі користувача.

Цей модуль налаштовує відображення, фільтрацію, пошук та редагування
кастомної моделі `User` в адмінці Django, адаптуючи стандартний `UserAdmin`
під авторизацію за допомогою `email`.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from account.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Конфігурація відображення моделі User в адміністративній панелі Django.

    Перевизначає стандартні набори полів (fieldsets), списки відображення,
    сортування та фільтри з урахуванням відсутності поля 'username' та
    наявності поля 'phone'.
    """

    # Поля, які відображаються у списку всіх користувачів
    list_display: tuple[str, ...] = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "is_staff",
        "is_active",
    )

    save_on_top: bool = True

    # Фільтри на правій панелі
    list_filter: tuple[str, ...] = ("is_staff", "is_superuser", "is_active")

    # Поля, за якими доступний текстовий пошук
    search_fields: tuple[str, ...] = ("email", "first_name", "last_name", "phone")

    # Порядок сортування в адмінці за замовчуванням
    ordering: tuple[str, ...] = ("email",)

    # Налаштування груп полів при редагуванні існуючого користувача
    fieldsets: tuple[tuple[str | None, dict[str, tuple[str, ...]]], ...] = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone")}),
        (
            (_("Permissions")),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    # Налаштування полів для форми створення нового користувача
    add_fieldsets: tuple[tuple[str | None, dict[str, tuple[str, ...]]], ...] = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone",
                    "password",
                ),
            },
        ),
    )
