from django.contrib import admin
from django.urls import URLResolver, path, include
from django.conf import settings
from django.conf.urls.static import static

from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns: list[URLResolver] = [
    path("admin/", admin.site.urls),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("", include("main.urls", namespace="main")),
    path("catalog/", include("goods.urls", namespace="goods")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("checkout/", include("order.urls", namespace="checkout")),
    path("pages/", include("pages.urls", namespace="pages")),
    path("feedback/", include("feedback.urls", namespace="feedback")),
    path("account/", include("account.urls", namespace="account")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
