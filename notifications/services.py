"""Модуль сервісу оркестрації сповіщень.

Цей модуль містить бізнес-логіку для масової або послідовної відправки
сповіщень через різні канали (обробники), що підтримують інтерфейс
`BaseNotificationHandler`.
"""

import logging
from typing import Any

from .handlers import BaseNotificationHandler


logger: logging.Logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, handlers: list[BaseNotificationHandler]) -> None:
        """
        Ініціалізує сервіс списком обробників.

        Args:
            handlers (list[BaseNotificationHandler]): Список екземплярів обробників,
            через які здійснюватиметься розсилка сповіщень.
        """
        self.handlers: list[BaseNotificationHandler] = handlers

    def notify(
        self,
        template_name_text: str,
        context: dict[str, Any],
        template_name_html: str = None,
        **kwargs: Any,
    ) -> None:
        """
        Відправляє сповіщення через усі зареєстровані хандлери.

        Усі додаткові параметри (email, phone, subject, telegram_id тощо)
        передаються динамічно через **kwargs.
        """
        for handler in self.handlers:
            try:
                handler.send(
                    template_name_text=template_name_text,
                    context=context,
                    template_name_html=template_name_html,
                    **kwargs,
                )
            except Exception as e:
                logger.error(
                    "Не вдалося відправити сповіщення через %s: %s",
                    handler.__class__.__name__,
                    e,
                )
