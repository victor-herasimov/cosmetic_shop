from django.urls import URLResolver, path
from .views import CartAddView

app_name: str = "cart"

urlpatterns: list[URLResolver] = [
    path("add/", CartAddView.as_view(), name="cart_add"),
]
