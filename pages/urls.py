"""
Модуль маршрутизації (URL-конфігурація) для додатка Додаткових сторінок.

Визначає точки доступу (endpoints) для відображення додаткових сторінок.
"""

from django.urls import URLResolver, path
from pages.views import DocumentView, ContactView


app_name: str = "pages"

urlpatterns: list[URLResolver] = [
    path("contact/", ContactView.as_view(), name="contact"),
    path("<slug:doc_type>/", DocumentView.as_view(), name="document"),
]
