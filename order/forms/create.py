"""
Цей модуль містить форму для створення замовлення.
"""

from django import forms
from validators import PhoneNumberValidator
from order.models import Order, DeliveryMethod, PaymentMethod


class CreateOrderForm(forms.ModelForm):
    """
    Форма для створення замовлення.
    """

    phone = forms.CharField(validators=[PhoneNumberValidator()])
    delivery_method = forms.ModelChoiceField(
        queryset=DeliveryMethod.objects.all(),
        empty_label=True,
        widget=forms.RadioSelect,
        initial=DeliveryMethod.objects.first(),
    )
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all(),
        empty_label=True,
        widget=forms.RadioSelect,
        initial=PaymentMethod.objects.first(),
    )

    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        """Мета-параметри форми замовлення."""

        model = Order
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "delivery_method",
            "payment_method",
            "city",
            "delivery_address",
            "comment",
        ]
