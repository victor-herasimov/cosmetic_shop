"""
Пакет допоміжних класів та міксинів (mixins) проєкту.

Об'єднує та експортує утиліти для розширення функціоналу моделей
(штампи часу, роботу зі слагами) та контролерів (обмеження HTMX-запитів),
дозволяючи імпортувати їх централізовано.
"""

from .date import DateMixin
from .slug import SlugMixin
from .only_htmx_mixin import OnlyHtmxMixin


__all__ = ["DateMixin", "SlugMixin", "OnlyHtmxMixin"]
