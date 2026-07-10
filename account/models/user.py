"""
Модуль користувацької моделі автентифікації для Django.

Цей модуль перевизначає стандартну модель користувача Django, дозволяючи
використовувати адресу електронної пошти (email) як основний ідентифікатор
для входу замість імені користувача (username). Включає кастомний менеджер
для коректного створення звичайних користувачів та суперкористувачів.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from mixins import DateMixin
from validators import PhoneNumberValidator


class UserManager(BaseUserManager):
    """
    Менеджер для кастомної моделі користувача.

    Забезпечує логіку створення користувачів та суперкористувачів
    з використанням email як унікального ідентифікатора.
    """

    def create_user(self, email, password=None, **kwargs) -> "User":
        """
        Створює, зберігає та повертає користувача з вказаним email та паролем.

        Обов'язково перевіряє наявність email та пароля. Автоматично
        нормалізує доменну частину адреси електронної пошти.
        """
        if not email:
            raise ValueError("Users must have a email")
        if not password:
            raise ValueError("Users must have a password")
        user: "User" = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs) -> "User":
        """
        Створює, зберігає та повертає суперкористувача (адміністратора).

        Автоматично виставляє прапорці доступу `is_staff`, `is_superuser`
        та `is_active` в True, якщо вони не були передані явно.
        """
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        user: "User" = self.create_user(email, password=password, **kwargs)
        return user


class User(DateMixin, AbstractBaseUser, PermissionsMixin):
    """
    Кастомна модель користувача системи.

    Використовує `email` як USERNAME_FIELD. Наслідує `DateMixin` для трекінгу
    дати створення/оновлення, `AbstractBaseUser` для базової автентифікації
    та `PermissionsMixin` для інтеграції з вбудованою системою прав та груп Django.
    """

    first_name = models.CharField(max_length=255, verbose_name="Ім'я")
    last_name = models.CharField(max_length=255, verbose_name="Прізвище")
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        unique=True,
        blank=True,
        null=True,
        validators=[PhoneNumberValidator()],
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    is_active = models.BooleanField(default=True, verbose_name="Активний")
    is_staff = models.BooleanField(default=False, verbose_name="Співробітник")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self) -> str:
        """Повертає повне ім'я користувача або email, якщо ім'я не вказано."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email

    class Meta:
        """Мета-параметри моделі користувача."""

        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"
        ordering = ["email"]
