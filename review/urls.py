"""
Модуль маршрутизації (URL-конфігурація) для додатка відгуків.

Визначає точки доступу (endpoints) для відображення відгуків.
"""

from django.urls import URLResolver, path
from review.views import GetReviewPageView, ReviewCreateView, ReviewDeleteView


app_name: str = "review"

urlpatterns: list[URLResolver] = [
    path("<int:product_id>/create/", ReviewCreateView.as_view(), name="create"),
    path("<int:review_id>/delete/", ReviewDeleteView.as_view(), name="delete"),
    path("<int:product_id>/", GetReviewPageView.as_view(), name="page"),
]
