"""
Модуль бізнес-логіки (сервісного шару) для роботи із зворотнім зв`язком.
"""

from typing import Any
from feedback.models import Feedback


class FeedbackService:
    """
    Сервіс для керування життєвим циклом зворотнього зв`язку.
    """

    model = Feedback

    def _send_feedback_notifications(self, feedback_id: int) -> None:
        """Надсилає лист адміністратору про нове повідомлення."""
        # TODO Тут буде логіка відправлення листа через celery
        # transaction.on_commit(lambda: send_feedback_notification_task.delay(feedback_id))

    def create(self, data: dict[str, Any]) -> Feedback:
        """
        Створює нове повідомлення зворотнього зв`язку.
        І відправляє email адміністратору.
        """

        feedback: Feedback = self.model.objects.create(**data)
        self._send_feedback_notifications(feedback.id)

        return feedback
