"""
Модуль маршрутизації (URL-конфігурація) для додатка Додаткових сторінок.

Визначає точки доступу (endpoints) для відображення додаткових сторінок.
"""

from django.urls import URLResolver, path
from pages.views import DocumentView


app_name: str = "pages"

urlpatterns: list[URLResolver] = [
    path("<slug:doc_type>/", DocumentView.as_view(), name="document"),
]
