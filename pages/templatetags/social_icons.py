"""
Модуль кастомних тегів та фільтрів шаблонів Django для відображення іконок.

Цей модуль містить фільтр `social_icon`, який дозволяє динамічно
підставляти потрібний SVG-код для соціальних мереж у HTML-шаблонах.
"""

from django import template
from django.utils.safestring import SafeText, mark_safe

register = template.Library()

ICONS: dict[str, str] = {
    "telegram": (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"'
        ' stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2">'
        "</polygon></svg>"
    ),
    "viber": (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"'
        ' stroke-linejoin="round"><path d="M15.05 5A5 5 0 0 1 19 8.95M15.05 1A9 9 0 0 1 23 8.94m-1 7.98v3a2 2 0 0 1-2.18 2'
        " 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84"
        " 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0"
        ' 1 22 16.92z"></path></svg>'
    ),
    "instagram": (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"'
        ' stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1'
        ' 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>'
    ),
    "facebook": (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"'
        ' stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>'
    ),
}
DEFAULT_ICON: str = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
    'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle>'
    '<line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 '
    '15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'
)


@register.filter
def social_icon(value) -> SafeText:
    """
    Повертає безпечний HTML-код SVG-іконки для заданої соціальної мережі.
    """
    icon_key: str = str(value).strip().lower() if value else ""
    icon_svg: str = ICONS.get(icon_key, DEFAULT_ICON)
    return mark_safe(icon_svg)
