"""
Модуль налаштування адміністративної панелі для моделі зворотного зв'язку.

Забезпечує кастомизоване відображення заявок користувачів в адмінці Django,
включаючи кольорові бейджі для статусів та обмеження прав на створення записів.
"""

from typing import Literal

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import SafeText
from feedback.models import Feedback


@admin.register(Feedback)
class FeedbackReadOnlyAdmin(admin.ModelAdmin):
    """
    Адміністративний інтерфейс для перегляду та модерації заявок зворотного зв'язку.

    Клас конфігурує відображення списку, фільтрацію за статусами,
    кастомні HTML-елементи для візуалізації станів обробки та блокує
    можливість ручного додавання записів через інтерфейс адмін-панелі.
    """

    list_display = ["name", "phone", "subject", "status_badge", "created"]
    fields = ["status", "name", "phone", "email", "subject", "body"]
    list_filter = ["status"]

    @admin.display(description="Статус")
    def status_badge(self, obj) -> SafeText:
        """
        Генерує кастомний HTML-бейдж для візуального відображення статусу заявки.

        Для кожного статусу підбирається своя палітра кольорів (текст та фон),
        що дозволяє менеджерам швидше орієнтуватися у списку повідомлень.

        Args:
            obj (Feedback): Поточний екземпляр моделі Feedback.

        Returns:
            SafeText: Безпечний HTML-рядок, що містить тег span зі стилями.
        """
        colors: dict[str, tuple[str, str]] = {
            Feedback.StatusChoices.NEW: ("#d1ecf1", "#0c5460"),
            Feedback.StatusChoices.IN_PROGRESS: ("#fff3cd", "#856404"),
            Feedback.StatusChoices.WAITING: ("#e2e3e5", "#383d41"),
            Feedback.StatusChoices.RESOLVED: ("#d4edda", "#155724"),
            Feedback.StatusChoices.SPAM: ("#f8d7da", "#721c24"),
            Feedback.StatusChoices.CLOSED: ("#e9ecef", "#6c757d"),
        }

        bg_color, text_color = colors.get(obj.status, ("#e2e3e5", "#383d41"))

        return format_html(
            '<span style="background-color: {}; color: {}; '
            "padding: 4px 8px; border-radius: 4px; "
            'font-weight: bold; font-size: 12px; display: inline-block;">'
            "{}</span>",
            bg_color,
            text_color,
            obj.get_status_display(),
        )

    def has_add_permission(self, request) -> Literal[False]:
        """
        Забороняє додавання нових заявок через інтерфейс адміністратора.

        Args:
            request (HttpRequest): Об'єкт поточного HTTP-запиту.

        Returns:
            Literal[False]: Завжди повертає False для блокування кнопки додавання.
        """
        return False
