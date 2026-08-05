from collections.abc import Iterable
from typing import Any
from urllib import request

from django.db.models import (
    F,
    Q,
    Count,
    Exists,
    ExpressionWrapper,
    FloatField,
    OuterRef,
    TextField,
    Value,
)
from django.db.models.functions import Concat
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet
from django.http import HttpRequest

from goods.forms import ProductSortForm
from goods.models import Product
from goods.models.brand import Brand
from goods.models.category import Category
from goods.models.characteristic import Characteristic
from goods.models.characteristic_item import CharacteristicItem
from wishlist.models import Favorite


class ProductService:

    SORT_MAPPING = {
        "default": "-updated",
        "name_asc": "title",
        "name_desc": "-title",
        "price_asc": "price",
        "price_desc": "-price",
        "bestsellers_asc": "is_bestseller",
        "bestsellers_desc": "-is_bestseller",
    }

    def __init__(self, request: HttpRequest) -> None:
        """
        Приймає request.GET або будь-який аналогічний словник параметрів.
        Це робить сервіс повністю незалежним від самого об'єкта request.
        """
        self.request = request
        self.params: dict[str, str] = self.request.GET
        self.sort_form: ProductSortForm = ProductSortForm(self.params)

        self.selected_categories: str = self.params.getlist("category")
        self.selected_brands: str = self.params.getlist("brand")
        self.price_min: str = self.params.get("price_min")
        self.price_max: str = self.params.get("price_max")

        self.char_filters: dict[int, list[str]] = {}
        for key, values in self.params.lists():
            if key.startswith("char_"):
                try:
                    item_id = int(key.split("_")[1])
                    self.char_filters[item_id] = values
                except ValueError:
                    continue

    def _annotate_current_price(self, queryset) -> QuerySet[Product]:
        """Внутрішній метод для підрахунку ціни зі знижкою."""

        return queryset.annotate(
            current_price=ExpressionWrapper(
                F("price") * (1.0 - (F("discount") / 100.0)),
                output_field=FloatField(),
            )
        )

    def _get_favorite_subquery(self) -> QuerySet[Favorite]:
        return Favorite.objects.filter(
            user=self.request.user, product_id=OuterRef("pk")
        )

    def _get_price_q_object(self) -> Q:
        """Будує базовий Q-об'єкт для фільтрації по ціні."""
        price_q = Q()
        if self.price_min:
            price_q &= Q(current_price__gte=self.price_min)
        if self.price_max:
            price_q &= Q(current_price__lte=self.price_max)
        return price_q

    def get_filtered_products(self):
        """Повертає фінальний відфільтрований QuerySet товарів для каталогу."""
        if self.sort_form.is_valid():
            sort_by = self.sort_form.cleaned_data.get("sort")
            order_field = self.SORT_MAPPING.get(sort_by, "-updated")
        else:
            order_field = "-updated"

        queryset: QuerySet[Product] = self._annotate_current_price(
            self.get_all(order=order_field)
        )

        if self.selected_categories:
            queryset = queryset.filter(cateogry__id__in=self.selected_categories)

        if self.selected_brands:
            queryset = queryset.filter(brand__id__in=self.selected_brands)

        for item_id, values in self.char_filters.items():
            queryset = queryset.filter(
                characteristics__item__id=item_id, characteristics__value__in=values
            )

        if self.price_min:
            queryset = queryset.filter(current_price__gte=self.price_min)
        if self.price_max:
            queryset = queryset.filter(current_price__lte=self.price_max)

        return queryset.distinct()

    def get_facets(self) -> dict[str, Any]:
        """Рахує багатовимірні лічильники для сайдбару."""
        base_products: QuerySet[Product] = self._annotate_current_price(self.get_all())

        price_q = self._get_price_q_object()

        category_facet_products = base_products.filter(price_q)
        if self.selected_brands:
            category_facet_products = category_facet_products.filter(
                brand__id__in=self.selected_brands
            )

        for item_id, values in self.char_filters.items():
            category_facet_products = category_facet_products.filter(
                characteristics__item__id=item_id, characteristics__value__in=values
            )

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

        brand_facet_products = base_products.filter(price_q)
        if self.selected_categories:
            brand_facet_products = brand_facet_products.filter(
                cateogry__id__in=self.selected_categories
            )
        for item_id, values in self.char_filters.items():
            brand_facet_products = brand_facet_products.filter(
                characteristics__item__id=item_id, characteristics__value__in=values
            )

        brands_query = Brand.objects.annotate(
            total_products=Count(
                "products", filter=Q(products__in=brand_facet_products), distinct=True
            )
        ).order_by("name")

        brands_data = []
        for b in brands_query:
            is_selected = str(b.id) in self.selected_brands
            brands_data.append(
                {
                    "id": b.id,
                    "name": b.name,
                    "count": b.total_products,
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
            if self.selected_brands:
                facet_products = facet_products.filter(
                    brand__id__in=self.selected_brands
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

        return {
            "price_min": self.price_min or "",
            "price_max": self.price_max or "",
            "categories": categories_data,
            "brands": brands_data,
            "grouped_characteristics": grouped_characteristics,
        }

    def get_all(self, order: str | None = None) -> QuerySet[Product]:
        """
        Повертає кверісет з усіма продуктами
        """
        result = (
            Product.objects.select_related("cateogry", "brand")
            .prefetch_related("fotos", "characteristics")
            .all()
        )
        if order:
            result = result.order_by(order)

        if self.request.user.is_authenticated:
            result = result.annotate(is_favorite=Exists(self._get_favorite_subquery()))
        return result

    def get_by_id(self, product_id: int) -> Product:
        """
        Повертає товар по йго ID.
        """
        if self.request.user.is_authenticated:
            return Product.objects.annotate(
                is_favorite=Exists(self._get_favorite_subquery())
            ).get(id=product_id)

        return Product.objects.get(id=product_id)

    def get_favorites(self) -> QuerySet[Product]:
        """Повертає кверісет з бажаними товарами для користувача"""
        return (
            Product.objects.filter(favorites__user=self.request.user)
            .annotate(is_favorite=Exists(self._get_favorite_subquery()))
            .select_related("cateogry", "brand")
            .prefetch_related("fotos")
            .order_by("-updated")
        )

    def get_bestsellers(self) -> QuerySet[Product]:
        """
        Повертає кверісет з першими 4-ма продуктами, що є хітом продаж. Якщо таких менше 4-х
        то добавляє іншими продуктами.
        """
        if self.request.user.is_authenticated:
            return (
                Product.objects.annotate(
                    is_favorite=Exists(self._get_favorite_subquery())
                )
                .select_related("cateogry", "brand")
                .prefetch_related("fotos")
                .order_by("-is_bestseller", "-updated")[:4]
            )
        return (
            Product.objects.select_related("cateogry")
            .prefetch_related("fotos")
            .order_by("-is_bestseller", "-updated")[:4]
        )

    def get_news(self) -> QuerySet[Product]:
        """
        Повертає кверісет з першими 4-ма новими продуктами.
        """
        if self.request.user.is_authenticated:
            return (
                Product.objects.annotate(
                    is_favorite=Exists(self._get_favorite_subquery())
                )
                .select_related("cateogry")
                .prefetch_related("fotos")
                .order_by("-is_new", "-created")[:4]
            )
        return (
            Product.objects.select_related("cateogry")
            .prefetch_related("fotos")
            .order_by("-is_new", "-created")[:4]
        )

    def get_by_slug(self, slug: str) -> Product:
        """
        Повертає Продукт, що відповідє слагу. Якщо такого не має то викидає виключення Product.DoesNotExist.
        """
        if self.request.user.is_authenticated:
            return (
                Product.objects.annotate(
                    is_favorite=Exists(self._get_favorite_subquery())
                )
                .select_related("cateogry")
                .prefetch_related("fotos", "characteristics__item")
                .get(slug=slug)
            )
        return (
            Product.objects.select_related("cateogry")
            .prefetch_related("fotos", "characteristics__item")
            .get(slug=slug)
        )

    def search(self, query: str, order: str | None = None) -> QuerySet[Product]:
        """
        Повертає прдукти, що містять запит query в заголовку або описі.
        """
        if len(query) > 0:
            results = (
                Product.objects.annotate(
                    search_text=Concat(
                        "title", Value(" "), "description", output_field=TextField()
                    )
                )
                .annotate(similarity=TrigramSimilarity("search_text", query))
                .filter(similarity__gt=0.007)
                .order_by("-similarity")
            )
            if order:
                results = results.order_by(order)

            if self.request.user.is_authenticated:
                results = results.annotate(
                    is_favorite=Exists(self._get_favorite_subquery())
                )
            return results

        return Product.objects.none()

    def get_similar_products(self, product: Product) -> QuerySet[Product]:
        """
        Повертає продукти, що подібні до продукта в якого слаг дорівнює product_slug.
        """
        current_char_ids = product.characteristics.values_list("id", flat=True)
        similar_products = (
            Product.objects.filter(characteristics__in=current_char_ids)
            .exclude(id=product.id)
            .annotate(same_chars_count=Count("characteristics"))
            .order_by("-same_chars_count", "?")
            .select_related("cateogry")
            .prefetch_related("characteristics__item", "fotos")[:4]
        )
        if self.request.user.is_authenticated:
            similar_products = similar_products.annotate(
                is_favorite=Exists(self._get_favorite_subquery())
            )
        return similar_products

    def get_products_by_ids(self, ids: Iterable[int]) -> QuerySet[Product]:
        """
        Повертає кверісет з продуктів id яких міститься в списку ids.
        """
        if self.request.user.is_authenticated:
            return (
                Product.objects.annotate(
                    is_favorite=Exists(self._get_favorite_subquery())
                )
                .prefetch_related("fotos")
                .filter(id__in=ids)
            )
        return Product.objects.prefetch_related("fotos").filter(id__in=ids)
