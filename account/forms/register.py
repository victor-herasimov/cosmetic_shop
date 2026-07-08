"""
Модуль форм автентифікації та реєстрації користувачів.

Містить кастомні форми Django, що розширюють базові механізми
автентифікації для роботи з додатковими полями користувача,
такими як номер телефону.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm

from validators import PhoneNumberValidator


User: type[AbstractUser] = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """
    Форма для реєстрації нового користувача в системі.

    Розширює стандартну `UserCreationForm`, додаючи обов'язкову
    валідацію номера телефону за допомогою кастомного валідатора,
    а також автоматично включає базові поля профілю (email, ім'я, прізвище).
    """

    phone = forms.CharField(validators=[PhoneNumberValidator()])

    class Meta(UserCreationForm.Meta):
        """
        Метадані форми реєстрації користувача.

        Наслідує `UserCreationForm.Meta` для автоматичної та безпечної
        інтеграції полів `password1` та `password2` без прямого
        декларування їх у списку `fields`.
        """

        model = User
        fields = (
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "phone",
        )
