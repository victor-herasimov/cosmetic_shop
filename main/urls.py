from django.urls import URLResolver, path
from .views import MainView

app_name: str = "main"

urlpatterns: list[URLResolver] = [
    path("", MainView.as_view(), name="index"),
]
