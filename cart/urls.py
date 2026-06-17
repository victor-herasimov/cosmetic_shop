from django.urls import URLResolver, path
from .views import CartAddView, CartRemoveView, CartUpdateView

app_name: str = "cart"

urlpatterns: list[URLResolver] = [
    path("add/", CartAddView.as_view(), name="cart_add"),
    path("remove/", CartRemoveView.as_view(), name="cart_remove"),
    path("update/", CartUpdateView.as_view(), name="cart_update"),
]
