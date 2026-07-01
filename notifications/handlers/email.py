"""
Модуль містить обробники для відправки сповіщень через канал Email.

Забезпечує рендеринг текстових та HTML-шаблонів за допомогою рушія Django
та їх безпосередню відправку кінцевим користувачам.
"""

import logging
from typing import Any
from django.core.mail import send_mail
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.conf import settings
from .base import BaseNotificationHandler

logger: logging.Logger = logging.getLogger(__name__)


class EmailNotificationHandler(BaseNotificationHandler):
    """
    Обробник для надсилання сповіщень електронною поштою (Email).

    Наслідується від `BaseNotificationHandler`. Використовує вбудовану
    функцію Django `send_mail` для відправки повідомлень, підтримує
    текстові та HTML-шаблони.
    """

    def send(
        self,
        template_name_text: str,
        context: dict[str, Any],
        template_name_html: str | None = None,
        **kwargs: Any
    ) -> None:
        """
        Рендерить шаблони сповіщення та надсилає email адресату.
        Args:
            template_name_text (str): Шлях до шаблону повідомлення.
            context (dict[str, Any]): Словник зі змінними для підстановки в шаблон.
            template_name_html (str): Шлях до html шаблону повідомлення. По замовчуванню None.
            kwargs: додаткові аргументи такі як email або phone, subject якщо потрібно,
        """
        email = kwargs.get("email")
        subject = kwargs.get("subject", "Нове сповіщення")

        if not email:
            return

        try:
            text_message: str = render_to_string(template_name_text, context)
        except TemplateDoesNotExist as e:
            logger.error(
                "Обов'язковий текстовий шаблон %s не знайдено.", template_name_text
            )
            raise e

        html_message: str | None = None
        if template_name_html:
            try:
                html_message = render_to_string(template_name_html, context)
            except TemplateDoesNotExist:
                logger.debug(
                    "HTML-шаблон для %s не знайдено, надсилається лише текст.",
                    template_name_html,
                )
        try:
            send_mail(
                subject=subject,
                message=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            logger.critical(
                "Неочікувана помилка в EmailNotificationHandler: %s", e, exc_info=True
            )
            raise e
