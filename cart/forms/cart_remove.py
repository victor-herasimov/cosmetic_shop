from django import forms


class CartRemoveForm(forms.Form):
    """
    Форма для видалення продукту з кошика.
    """

    product_id = forms.IntegerField(required=True)
