"""
Модуль для роботи з формами додатку зворотного зв'язку.

Містить класи форм, які забезпечують валідацію вхідних даних від користувачів
та їх подальше збереження в базу даних через Django ORM.
"""

from django import forms
from feedback.models import Feedback


class FeedbackForm(forms.ModelForm):
    """
    Форма для відправки повідомлень зворотного зв'язку користувачами сайту.

    Автоматично генерує HTML-поля на основі моделі `Feedback`, застосовує
    встановлені в моделі обмеження (max_length, choices) та запускає
    кастомні валідатори (наприклад, для перевірки номера телефону).
    """

    class Meta:
        """Мета-параметри форми FeedbackForm."""

        model = Feedback
        fields = ["name", "email", "phone", "subject", "body"]
