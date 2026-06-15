from django import forms
from django.core.validators import MinValueValidator


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(validators=[MinValueValidator(1)])
    override = forms.BooleanField(required=False, initial=False)
