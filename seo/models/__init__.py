"""
Ініціалізаційний модуль пакета моделей.

Експортує модель `SEOPage` для зручного імпорту з кореня пакета
(наприклад, `from seo.models import SEOPage`), приховуючи
внутрішню структуру файлів.
"""

from .seo_page import SEOPage

__all__ = ["SEOPage"]
