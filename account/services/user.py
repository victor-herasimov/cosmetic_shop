"""Модуль сервісів для додатку автентифікації та облікових записів (account).

Цей модуль містить класи та функції бізнес-логіки, які керують життєвим циклом
користувачів, їхніми профілями та супутніми операціями. Він виступає посередником
між Django Views/Forms та Django ORM, забезпечуючи дотримання принципу
єдиної відповідальності (Single Responsibility Principle).

Доступні класи:
    UserService: Набір методів для створення, оновлення та керування користувачами.
"""

from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

User: type[AbstractUser] = get_user_model()


class UserService:
    """Сервісний шар для керування бізнес-логікою, пов'язаною з користувачами.

    Цей клас інкапсулює операції над моделлю користувача, відокремлюючи
    логіку бази даних та обробки даних від Django Views (контролерів).
    """

    @classmethod
    def create(cls, data: dict[str, Any]) -> AbstractUser:
        """Створює нового користувача в системі із захешованим паролем.

        Метод копіює вхідні дані, очищає їх від технічних полів форми реєстрації
        (таких як `password1` та `password2`), безпечно створює запис у базі даних
        через `create_user` та прив'язує автентифікаційний бекенд для спрощення
        подальшого процесу авторизації (автологіну).

        Args:
            data (dict[str, Any]): Словник з даними користувача, зазвичай отриманий
                із `form.cleaned_data`. Повинен містити обов'язкові поля моделі
                (наприклад, `username`) та технічні поля `password1` і `password2`.

        Returns:
            AbstractUser: Екземпляр створеної моделі користувача (актуальної для
                поточного Django-проєкту).

        Raises:
            ValidationError: Якщо дані не проходять внутрішню валідацію моделі Django.
            IntegrityError: Якщо користувач із такому унікальним полем (наприклад,
                `username` або `email`) вже існує.
        """
        user_data: dict[str, Any] = data.copy()

        user_data.pop("password1", None)
        raw_password: str = user_data.pop("password2", None)

        user: AbstractUser = User.objects.create_user(
            password=raw_password, **user_data
        )

        user.backend = "django.contrib.auth.backends.ModelBackend"
        return user
