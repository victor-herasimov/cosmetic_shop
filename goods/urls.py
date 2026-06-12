from django.urls import URLResolver, path
from .views import CatalogView

app_name: str = "goods"

urlpatterns: list[URLResolver] = [
    path("", CatalogView.as_view(), name="catalog"),
]
