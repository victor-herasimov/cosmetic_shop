"""
Модуль форм для керування профілем користувача.

Цей модуль містить форму, що забезпечує валідацію та збереження даних,
пов'язаних із профілем користувача, зокрема зміну персональних даних.
"""

from django import forms
from django.contrib.auth import get_user_model
from account.models import User as CustomUser


User: type[CustomUser] = get_user_model()


class ChangeUserPhoneForm(forms.ModelForm):
    """
    Форма для безпечної зміни номера телефону користувача.
    """

    phone = forms.CharField()

    class Meta:
        """
        Мета-параметри форми зміни імені.
        """

        model = User
        fields = ("phone",)
