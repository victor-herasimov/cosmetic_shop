"""Модуль для валідації специфічних форматів даних у Django.

Містить класи та інструменти для перевірки відповідності полів моделей
або форм визначеним бізнес-правилам.
"""

import re
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class PhoneNumberValidator:
    """Валідатор для перевірки відповідності номера телефону заданому шаблону.

    Клас дозволяє валідувати номери телефонів за допомогою регулярних виразів.
    За замовчуванням використовується український або міжнародний формат:
    +** (***) ***-**-**. Завдяки декоратору `@deconstructible`, об'єкт класу
    може бути коректно серіалізований у міграціях Django.

    Attributes:
        message (str): Текст повідомлення про помилку, якщо валідація провалена.
        code (str): Код помилки для ідентифікації в Django (наприклад, для forms.ValidationError).
        pattern (str): Регулярний вираз, за яким перевіряється номер телефону.
    """

    message = "Номер телефону повинен мати формат: +** (***) ***-**-**!"
    code = "phone"
    pattern = r"^\+\d{2} \(\d{3}\) \d{3}-\d{2}-\d{2}$"

    def __init__(self, message=None, code=None, pattern=None):
        """Ініціалізує екземпляр валідатора з можливістю кастомізації параметрів.

        Args:
            message (str, optional): Кастомне повідомлення про помилку.
            code (str, optional): Кастомний код помилки.
            pattern (str, optional): Кастомний регулярний вираз для перевірки.
        """
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if pattern is not None:
            self.pattern = pattern

    def __call__(self, value):
        """Виконує перевірку переданого значення номера телефону.

        Args:
            value (str): Номер телефону для валідації.

        Raises:
            ValidationError: Якщо `value` не відповідає регулярному виразу `pattern`.
        """
        prog = re.compile(self.pattern)
        result = re.match(prog, value)
        if not result:
            raise ValidationError(
                message=self.message, code=self.code, params={"value": value}
            )

    def __eq__(self, other):
        """Перевіряє рівність двох екземплярів валідатора."""
        return (
            isinstance(other, PhoneNumberValidator)
            and (self.message == other.message)
            and (self.code == other.code)
            and (self.pattern == other.pattern)
        )
