from django.views.generic import ListView

from goods.services import ProductService
from mixins.only_htmx_mixin import OnlyHtmxMixin


class LiveSearchView(OnlyHtmxMixin, ListView):
    """
    Представлення для відображення живого пошуку.
    """

    template_name = "goods/includes/live_search.html"
    context_object_name = "products"

    def get_queryset(self):
        """
        Повертає відфільтрований список товарів для каталогу.
        """
        search_text: str | None = self.request.GET.get("search", "")
        return ProductService().search(search_text)[:10]
