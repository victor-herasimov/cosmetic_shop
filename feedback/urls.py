"""
Модуль маршрутизації (URL-конфігурація) для додатка зворотнього зв`язку.

Визначає точки доступу (endpoints) для керування створенням зворотньго зв`язку.
"""

from django.urls import URLResolver, path
from feedback.views import FeedbackCreateView


app_name: str = "feedback"

urlpatterns: list[URLResolver] = [
    path("create/", FeedbackCreateView.as_view(), name="create"),
]
