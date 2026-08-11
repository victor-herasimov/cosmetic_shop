"""
Модуль forms для обробки та валідації форм відгуків.

Містить форми, необхідні для створення та редагування відгуків
користувачів про товари.
"""

from django import forms

from review.models import Review


class ReviewCreateForm(forms.ModelForm):
    """
    Форма для створення нового відгуку про товар.

    Використовує кастомний віджет радіо-кнопок для вибору рейтингу від 1 до 5.
    Поле продукту передається через приховане поле,
    а прив'язка до користувача відбувається на рівні контролера з міркувань безпеки.
    """

    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
    )

    class Meta:
        """Метадані форми для зв'язку з моделлю Review."""

        model = Review
        fields = ["rating", "text"]
