from django import forms


class ProductSortForm(forms.Form):
    SORT_CHOICES = [
        ("default", "По замовчуванню"),
        ("name_asc", "По алфавіту(збільшшення)"),
        ("name_desc", "По алфавіту(зменшення)"),
        ("price_asc", "Ціна (від дешевших)"),
        ("price_desc", "Ціна (від дорогих)"),
        ("bestsellers_asc", "По популярності(збільшення)"),
        ("bestsellers_desc", "По популярності(зменшення)"),
    ]

    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label="Сортувати:",
        widget=forms.Select(),
    )
