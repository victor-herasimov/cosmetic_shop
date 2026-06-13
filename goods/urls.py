from django.urls import URLResolver, path
from .views import CatalogView, LiveSearchView

app_name: str = "goods"

urlpatterns: list[URLResolver] = [
    path("", CatalogView.as_view(), name="catalog"),
    path("search/live/", LiveSearchView.as_view(), name="live_search"),
]
