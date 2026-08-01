"""Модуль містить форму для фільтрації замовлент в особистому кабінеті"""

from django import forms


class OrderFilterForm(forms.Form):
    """Форма для фільтрації замовлент в особистому кабінеті"""

    FILTER_CHOICES = [
        ("all", "Всі"),
        ("new", "Новe"),
        ("in_progress", "В обробці"),
        ("shipped", "Відправлено"),
        ("delivered", "Доставлено"),
        ("completed", "Виконано"),
        ("canceled", "Відмінено"),
    ]

    filter = forms.ChoiceField(
        choices=FILTER_CHOICES,
        required=False,
        label="Статус замовлення:",
        widget=forms.Select(),
    )
