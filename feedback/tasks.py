"""
Модуль асинхронних завдань для системи зворотного зв'язку (Feedback).

Містить Celery-завдання для обробки та відправки Email-сповіщень
адміністраторам сайту про нові повідомлення користувачів.
"""

import logging
from typing import Any
from celery import shared_task

from feedback.models import Feedback
from main.models import SiteConfig
from main.services import SiteConfigService
from notifications.handlers import EmailNotificationHandler
from notifications.services import NotificationService


logger: logging.Logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_feedback_notification_task(self, feedback_id: int, base_url: str) -> None:
    """
    Асинхронно відправляє Email-сповіщення адміністратору про новий фідбек.

    Завдання отримує актуальні налаштування сайту для визначення email адреси
    отримувача. У випадку мережевих збоїв або помилок поштового сервера,
    завдання автоматично повторюється (до 3 разів з інтервалом у 60 секунд).

    Args:
        self: Екземпляр Celery-завдання (завдяки bind=True).
        feedback_id (int): Первинний ключ (ID) об'єкта Feedback у базі даних.
        base_url (str): Базовий URL сайту (наприклад, https://mybeauty.com)
            для формування абсолютних посилань у шаблоні листа.

    Returns:
        None

    Raises:
        self.retry: Викидається для планування повторної спроби Celery у разі помилки.
    """

    feedback: Feedback = Feedback.objects.filter(pk=feedback_id).first()

    if feedback is None:
        logger.error("Повідомлення №%s не знайдено в БД.", feedback_id)
        return

    notifications_service: NotificationService = NotificationService(
        handlers=[EmailNotificationHandler()]
    )

    config: SiteConfig = SiteConfigService().get()

    context: dict[str, Any] = {
        "config": config,
        "feedback": feedback,
        "base_url": base_url,
    }
    # TODO add admin email from db
    try:
        # Відправка адміну
        notifications_service.notify(
            template_name_text="feedback/emails/email-admin-feedback.txt",
            context=context,
            template_name_html="feedback/emails/email-admin-feedback.html",
            email="admin@mybeauty.com",
            subject=f"Нове повідомлення зворотного зв'язку №{ feedback.id }",
        )

    except Exception as exc:
        if self.request.retries >= self.max_retries:
            logger.critical(
                "Вичерпано всі %s спроби відправки сповіщення №%s. Повідомлення не доставлено.",
                self.max_retries + 1,
                feedback_id,
            )
        else:
            logger.exception(
                "Помилка відправки листа для зворотного зв'язку %s. Спроба %s з %s. Повтор...",
                feedback_id,
                self.request.retries + 1,
                self.max_retries + 1,
            )
        raise self.retry(exc=exc)
