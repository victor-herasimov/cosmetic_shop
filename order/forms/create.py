"""
Цей модуль містить форму для створення замовлення.
"""

from django import forms
from validators import PhoneNumberValidator
from order.models import Order
from order.services import DeliveryMethodService, PaymentMethodService


class CreateOrderForm(forms.ModelForm):
    """
    Форма для створення замовлення.
    """

    phone = forms.CharField(validators=[PhoneNumberValidator()])
    delivery_method = forms.ModelChoiceField(
        queryset=DeliveryMethodService.get_actives(),
        empty_label=True,
        widget=forms.RadioSelect,
    )
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethodService().get_actives(),
        empty_label=True,
        widget=forms.RadioSelect,
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
