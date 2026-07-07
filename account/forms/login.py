"""
Модуль для кастомних форм автентифікації користувачів.

Містить форми, які розширюють стандартні механізми Django Auth для забезпечення
гнучкіших варіантів входу, таких як автентифікація за двома типами ідентифікаторів.
"""

import re
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class EmailOrPhoneLoginForm(AuthenticationForm):
    """
    Форма для автентифікації користувачів за допомогою Email або номера телефону.

    Розширює стандартну `AuthenticationForm`, дозволяючи користувачеві вводити
    як адресу електронної пошти, так і український номер телефону у полі `username`.
    Поле автоматично розпізнає тип даних та нормалізує його під формат бази даних.
    """

    username = forms.CharField(required=True)

    def clean_username(self) -> str:
        """
        Перевіряє та нормалізує поле `username`.

        Спочатку метод намагається провалідувати введені дані як Email. Якщо це пошта,
        вона приводиться до нижнього регістру. Якщо ні — дані розглядаються як номер
        телефону: з них видаляються всі символи, крім цифр, додається міжнародний код
        України (+380), і рядок форматується відповідно до стандарту, що зберігається в БД.

        Returns:
            str: Нормалізований email у нижньому регістрі або відформатований
                 номер телефону у вигляді '+38 (0XX) XXX-XX-XX'.

        Raises:
            ValidationError: Якщо введені дані не є коректним email-ом і не можуть
                             бути приведені до валідного українського номера телефону.
        """
        data: str = self.cleaned_data.get("username", "").strip()
        try:
            validate_email(data)
            return data.lower()
        except ValidationError:
            pass
        print("Hi clean")
        digits: str = re.sub(r"\D", "", data)

        if len(digits) == 10 and digits.startswith("0"):
            digits = "38" + digits
        elif len(digits) == 11 and digits.startswith("8"):
            digits = "3" + digits

        if len(digits) != 12 or not digits.startswith("380"):
            raise ValidationError(
                "Введіть коректний email або номер телефону (наприклад, 0960000000)."
            )

        formatted_phone: str = (
            f"+{digits[:2]} ({digits[2:5]}) {digits[5:8]}-{digits[8:10]}-{digits[10:12]}"
        )

        return formatted_phone
