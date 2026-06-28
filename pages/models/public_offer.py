"""
Модуль Публічної оферти сайту.
"""

from .base_legal_document import BaseLegalDocument


class PublicOffer(BaseLegalDocument):
    """
    Модель для керування Публічною офертою сайту.

    Успадковує поведінку синглтона та структуру текстових полів від `BaseLegalDocument`.
    Дозволяє адміністратору редагувати офіційний текст публічної оферти в одному екземплярі через адмін-панель.
    """

    class Meta:
        """Мета-параметри для відображення моделі в адмін-панелі Django."""

        app_label = "pages"
        verbose_name = "Публічна оферта"
        verbose_name_plural = "Публічна оферта"

    def __str__(self) -> str:
        """Повертає текстове представлення — заголовок Публічної оферти."""
        return self.title
