"""
Модуль бізнес-логіки (сервісного шару) для роботи із зворотнім зв`язком.
"""

from typing import Any

from django.http import HttpRequest
from feedback.models import Feedback
from feedback.tasks import send_feedback_notification_task


class FeedbackService:
    """
    Сервіс для керування життєвим циклом зворотнього зв`язку.
    """

    model = Feedback

    def __init__(self, request: HttpRequest) -> None:
        self.base_url = f"{request.scheme}://{request.get_host()}"

    def _send_feedback_notifications(self, feedback_id: int) -> None:
        """Надсилає лист адміністратору про нове повідомлення."""
        send_feedback_notification_task.delay(feedback_id, self.base_url)

    def create(self, data: dict[str, Any]) -> Feedback:
        """
        Створює нове повідомлення зворотнього зв`язку.
        І відправляє email адміністратору.
        """

        feedback: Feedback = self.model.objects.create(**data)
        self._send_feedback_notifications(feedback.id)

        return feedback
