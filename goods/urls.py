from django.urls import URLResolver, path
from .views import CatalogView, LiveSearchView, SearchView, ProductDetailView

app_name: str = "goods"

urlpatterns: list[URLResolver] = [
    path("", CatalogView.as_view(), name="catalog"),
    path("search/", SearchView.as_view(), name="search"),
    path("search/live/", LiveSearchView.as_view(), name="live_search"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="product"),
]
