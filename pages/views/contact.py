"""
Модуль для відображення сторінки контакту сайту.
"""

from typing import Any

from django.views.generic import TemplateView
from feedback.forms import FeedbackForm


class ContactView(TemplateView):
    """
    Представлення для відображення сторінки контактів.
    """

    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Додає до контексту заголовок сторінки title.
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "Контакти"
        context["feedback_form"] = FeedbackForm()

        return context
