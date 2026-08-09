"""
Модуль маршрутизації (URL-конфігурація) для додатка відгуків.

Визначає точки доступу (endpoints) для відображення відгуків.
"""

from django.urls import URLResolver, path
from review.views import GetReviewPageView


app_name: str = "review"

urlpatterns: list[URLResolver] = [
    path("<int:product_id>/", GetReviewPageView.as_view(), name="page"),
]
