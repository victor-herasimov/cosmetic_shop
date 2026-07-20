from typing import Any

from django.core.paginator import Page, Paginator
from django.db.models import F, Q, Count, ExpressionWrapper, FloatField, QuerySet
from django.http import Http404
from django.views.generic import ListView
from django.conf import settings

from goods.models.category import Category
from goods.models import Product, Characteristic
from goods.models.characteristic_item import CharacteristicItem
from goods.services import CategoryService, ProductService
from goods.forms import ProductSortForm


class CatalogView(ListView):
    """
    Представлення для відображення каталогу товарів.
    """

    # template_name = "goods/catalog.html"
    context_object_name = "products"
    paginate_by = settings.ITEMS_PER_PAGE

    SORT_MAPPING = {
        "default": "-updated",
        "name_asc": "title",
        "name_desc": "-title",
        "price_asc": "price",
        "price_desc": "-price",
        "bestsellers_asc": "is_bestseller",
        "bestsellers_desc": "-is_bestseller",
    }

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("HX-Request"):
            return ["goods/includes/_ajax_products.html"]
        return ["goods/catalog.html"]

    def annotate_current_price(self, queryset):
        """
        Динамічно вираховує ціну зі знижкою (у відсотках) на рівні бази даних.
        Створює поле 'current_price'.
        """
        return queryset.annotate(
            current_price=ExpressionWrapper(
                F("price") * (1.0 - (F("discount") / 100.0)),
                output_field=FloatField(),  # Переводимо у Float/Decimal для коректної фільтрації
            )
        )

    def get_queryset(self):
        """
        Повертає відфільтрований список товарів для каталогу.
        """
        form = ProductSortForm(self.request.GET)

        if form.is_valid():
            sort_by = form.cleaned_data.get("sort")
            order_field = self.SORT_MAPPING.get(sort_by, "-updated")
        else:
            order_field = "-updated"

        queryset: QuerySet[Product] = self.annotate_current_price(
            ProductService.get_all(order=order_field)
        )

        self.selected_categories = self.request.GET.getlist("category")
        self.price_min = self.request.GET.get("price_min")
        self.price_max = self.request.GET.get("price_max")

        self.char_filters = {}
        for key, values in self.request.GET.lists():
            if key.startswith("char_"):
                try:
                    item_id = int(key.split("_")[1])
                    self.char_filters[item_id] = values
                except ValueError:
                    continue

        if self.selected_categories:
            queryset = queryset.filter(cateogry__id__in=self.selected_categories)

        for item_id, values in self.char_filters.items():
            queryset = queryset.filter(
                characteristics__item__id=item_id, characteristics__value__in=values
            )

        if self.price_min:
            queryset = queryset.filter(current_price__gte=self.price_min)
        if self.price_max:
            queryset = queryset.filter(current_price__lte=self.price_max)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        """
        Повертає словник контексту для рендерингу шаблону.
        Будуємо багатовимірні фасети та додаємо їх у контекст.
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)

        base_products: QuerySet[Product] = self.annotate_current_price(
            ProductService.get_all()
        )

        price_q = Q()
        if self.price_min:
            price_q &= Q(current_price__gte=self.price_min)
        if self.price_max:
            price_q &= Q(current_price__lte=self.price_max)

        category_facet_products = base_products.filter(price_q)
        for item_id, values in self.char_filters.items():
            category_facet_products = category_facet_products.filter(
                characteristics__item__id=item_id, characteristics__value__in=values
            )

        # Рахуємо кількість товарів для кожної категорії
        categories_query = Category.objects.annotate(
            total_products=Count(
                "products",
                filter=Q(products__in=category_facet_products),
                distinct=True,
            )
        ).order_by("name")

        # Формуємо список категорій зі статусом checked/disabled для шаблону
        categories_data = []
        for cat in categories_query:
            is_selected = str(cat.id) in self.selected_categories
            categories_data.append(
                {
                    "id": cat.id,
                    "name": cat.name,
                    "count": cat.total_products,
                    "is_selected": is_selected,
                }
            )

        all_characteristic_items = CharacteristicItem.objects.prefetch_related(
            "items"
        ).all()
        grouped_characteristics = []

        for item in all_characteristic_items:
            # Будуємо QuerySet товарів, ігноруючи поточну групу характеристик
            facet_products: QuerySet[Product] = base_products.filter(price_q)

            if self.selected_categories:
                facet_products = facet_products.filter(
                    cateogry__id__in=self.selected_categories
                )

            for other_item_id, values in self.char_filters.items():
                if other_item_id != item.id:
                    facet_products = facet_products.filter(
                        characteristics__item__id=other_item_id,
                        characteristics__value__in=values,
                    )

            # Рахуємо кількість товарів для кожного значення поточної характеристики
            values_query = (
                Characteristic.objects.filter(item=item)
                .values("value")
                .annotate(
                    total=Count(
                        "products", filter=Q(products__in=facet_products), distinct=True
                    )
                )
                .order_by("value")
            )

            char_values = []
            for v in values_query:
                is_selected = str(v["value"]) in self.char_filters.get(item.id, [])
                char_values.append(
                    {
                        "value": v["value"],
                        "count": v["total"],
                        "is_selected": is_selected,
                    }
                )
            grouped_characteristics.append(
                {"id": item.id, "name": item.name, "values": char_values}
            )

        paginator: Paginator = context["paginator"]
        page_obj: Page = context["page_obj"]

        context["price_min"] = self.price_min or ""
        context["price_max"] = self.price_max or ""
        context["categories"] = categories_data
        context["grouped_characteristics"] = grouped_characteristics

        context["total_products"] = ProductService.get_products_count()

        context["elided_page_range"] = paginator.get_elided_page_range(
            number=page_obj.number, on_each_side=1, on_ends=1
        )
        context["order_form"] = ProductSortForm(self.request.GET)
        return context
