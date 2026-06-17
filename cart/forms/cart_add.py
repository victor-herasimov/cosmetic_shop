from django import forms
from django.core.validators import MinValueValidator


class CartAddForm(forms.Form):
    """
    Форма для додавання продукту до кошика.
    """

    CART_ACTIONS: list[tuple[str, str]] = [("add", "Додати"), ("subtract", "Відняти")]

    product_id = forms.IntegerField(required=True)
    quantity = forms.IntegerField(validators=[MinValueValidator(1)])
    override = forms.BooleanField(required=False, initial=False)

    action = forms.ChoiceField(choices=CART_ACTIONS, required=False)
