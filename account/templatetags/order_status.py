"""
Цей модуль містить фільтр співставлення css класа-модифікатора зі статусом замовлення.
"""

from django import template

register = template.Library()


@register.filter
def get_css_status(status: str) -> str:
    """
    Повертає css класс модифікатор в залежності від статусу замовлення
    """
    CSS_MAP: dict[str, str] = {
        "new": "order-badge--new",
        "in_progress": "order-badge--processing",
        "shipped": "order-badge--shipped",
        "delivered": "order-badge--delivered",
        "completed": "order-badge--completed",
        "canceled": "order-badge--cancelled",
    }

    return CSS_MAP.get(status, "")
