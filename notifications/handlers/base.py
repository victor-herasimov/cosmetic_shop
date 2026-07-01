"""Модуль для визначення базових інтерфейсів обробників сповіщень.

Цей модуль містить абстрактні класи, які задають єдиний стандарт для інтеграції
різних каналів сповіщень (наприклад, Email, SMS, Telegram тощо) в систему.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseNotificationHandler(ABC):
    """Абстрактний базовий клас для обробників сповіщень.

    Усі конкретні реалізації (EmailHandler, SMSHandler тощо) повинні успадковувати
    цей клас та реалізовувати його абстрактні методи.
    """

    @abstractmethod
    def send(
        self,
        template_name_text: str,
        context: dict[str, Any],
        template_name_html: str | None = None,
        **kwargs: Any
    ) -> None:
        """Відправляє сповіщення користувачеві на основі шаблону.

        Args:
            template_name_text (str): Шлях до шаблону повідомлення.
            context (dict[str, Any]): Словник зі змінними для підстановки в шаблон.
            template_name_html (str): Шлях до html шаблону повідомлення. По замовчуванню None.
            kwargs: додаткові аргументи такі як email або phone, subject якщо потрібно,

        """
