from django.http import HttpResponseBadRequest
from django.views.generic import ListView

from goods.services import ProductService


class LiveSearchView(ListView):
    """
    Представлення для відображення живого пошуку.
    """

    template_name = "goods/includes/live_search.html"
    context_object_name = "products"

    def dispatch(self, request, *args, **kwargs):
        """
        Перевіряємо, чи запит прийшов саме від HTMX
        """
        if not request.headers.get("HX-Request"):
            return HttpResponseBadRequest(
                "Цей URL доступний лише для AJAX/HTMX запитів"
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Повертає відфільтрований список товарів для каталогу.
        """
        search_text: str | None = self.request.GET.get("search", "")
        print(search_text)
        return ProductService().search(search_text)[:10]
