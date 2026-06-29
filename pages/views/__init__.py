"""
Пакет представлень (Views) для застосунку pages.

Цей файл експортує головні класи представлень на рівень пакета,
забезпечуючи чистіший та зручніший імпорт в інших модулях проєкту.
"""

from .document import DocumentView
from .contact import ContactView

__all__ = ["DocumentView", "ContactView"]
