from django import forms
from django.core.validators import MinValueValidator


class CartAddForm(forms.Form):
    """
    Форма для додавання продукту до кошика.
    """

    product_id = forms.IntegerField(required=True)
    quantity = forms.IntegerField(validators=[MinValueValidator(1)])
    override = forms.BooleanField(required=False, initial=False)
