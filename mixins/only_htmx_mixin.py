"""
Міксини для контролерів (Class-Based Views), що керують доступом до ендпоінтів.

Містить інструменти для фільтрації вхідних HTTP-запитів на основі специфічних
заголовків, зокрема для інтеграції з HTMX-архітектурою.
"""

from django.http import HttpResponseBadRequest


class OnlyHtmxMixin:
    """
    Забороняє всі запити крім HTMX/AJAX.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Перевіряємо, чи запит прийшов саме від HTMX
        """
        if not request.headers.get("HX-Request"):
            return HttpResponseBadRequest(
                "Цей URL доступний лише для AJAX/HTMX запитів"
            )
        return super().dispatch(request, *args, **kwargs)
