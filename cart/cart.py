import copy
from decimal import Decimal
from collections.abc import Iterable
from django.conf import settings
from django.db.models import QuerySet
from django.http import HttpRequest
from goods.models import Product
from goods.services.product import ProductService


type CartType = dict[str, dict[str, int | str | Product | Decimal]]


class Cart:
    """
    Корзина покупок
    """

    def __init__(self, request: HttpRequest) -> None:
        """
        Ініціалізувати корзину.
        """
        self.session = request.session
        cart: CartType = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart: CartType = cart

    def get_item_by_product(
        self, product: Product
    ) -> dict[str, int | str | Product | Decimal]:
        cart: CartType = copy.deepcopy(self.cart)
        cart_item = cart.get(str(product.id))
        if cart_item is None:
            return None
        cart_item["product"] = product
        cart_item["price"] = Decimal(cart_item["price"])
        cart_item["total_price"] = cart_item["price"] * cart_item["quantity"]
        return cart_item

    def add(
        self, product: Product, quantity: int = 1, override_quantity: bool = False
    ) -> None:
        """
        Додати продукт до кошика або оновити його кількість.
        """
        product_id: str = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.get_price_with_discount),
            }
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self) -> None:
        """
        Помітити сесію як 'змінену', щоб зберегти її
        """
        self.session.modified = True

    def remove(self, product: Product) -> None:
        """
        Видалення продукту з кошика
        """
        product_id: str = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Прокрутити товарні позиції в циклі і отримати продукти з бази даних.
        """
        product_ids: Iterable[str] = self.cart.keys()
        products: QuerySet[Product] = ProductService.get_products_by_ids(product_ids)
        cart: CartType = copy.deepcopy(self.cart)
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self) -> int:
        """
        Повертає кількість продуктів в корзині.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def __bool__(self) -> bool:
        """
        Повертає True якщо в кошику є товари, інакше False.
        """
        return bool(self.cart)

    def __contains__(self, item) -> bool:
        return item in self.cart

    def get_total_price(self) -> Decimal:
        """
        Повертає загальну суму кошика.
        """
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self) -> None:
        """
        Видаляє кошик з сеансу.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
