"""
Модуль для відображення сторінки контакту сайту.
"""

from typing import Any

from django.views.generic import TemplateView


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

        return context
