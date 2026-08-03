"""
Модуль контекст-процесорів та допоміжних функцій для улюблених об'єктів.

Призначений для підготовки даних про улюблені об'єкти користувача
та передачі їх у контекст шаблонів Django.
"""

from django.http import HttpRequest

from .services import FavoriteService


def user_has_favorite(request: HttpRequest) -> dict[str, bool]:
    """
    Повертає словник із прапорцем наявності улюблених об'єктів у користувача.

    Використовується як Django Context Processor для автоматичного
    додавання змінної `user_has_favorite` у контекст шаблонів.
    """
    return {"user_has_favorite": FavoriteService(request).has_favorite()}
