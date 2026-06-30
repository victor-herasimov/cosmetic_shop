"""
Модуль для роботи зі зворотним зв'язком користувачів.

Цей модуль містить Django-моделі та супутні структури даних,
необхідні для збереження, валідації та сортування повідомлень,
які користувачі відправляють через контактні форми на сайті.
"""

from django.db import models
from mixins import DateMixin
from validators import PhoneNumberValidator


class Feedback(DateMixin):
    """
    Модель для збереження повідомлень зворотного зв'язку від користувачів.

    Успадковує `DateMixin` для автоматичного логування дати створення
    та оновлення запису.

    Attributes:
        name (str): Ім'я користувача, який залишив відгук.
        email (str): Електронна адреса для зв'язку.
        phone (str): Номер телефону (валідується через PhoneNumberValidator).
        subject (str): Тема звернення (обрана з SubjectChoices).
        body (str): Текст повідомлення користувача.
    """

    class SubjectChoices(models.TextChoices):
        """Варіанти тем для звернення у формі зворотного зв'язку."""

        CONSULTATION = ("consultation", "Консультація щодо підбору догляду")
        QUESTION = ("question", "Питання щодо замовлення чи доставки")
        SUGGESTION = ("suggestion", "Пропозиція про співпрацю")
        OTHER = ("other", "Інше питання")

    name = models.CharField(max_length=256, verbose_name="Ім`я")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(
        max_length=19,
        verbose_name="Телефон",
        unique=False,
        validators=[PhoneNumberValidator()],
    )
    subject = models.CharField(
        max_length=12, choices=SubjectChoices.choices, verbose_name="Тема"
    )
    body = models.TextField(verbose_name="Повідомлення")

    class Meta:
        """Мета-параметри моделі Feedback."""

        verbose_name = "Зворотній зв`язок"
        verbose_name_plural = "Зворотній зв`язок"
        ordering = ["-created"]

    def __str__(self) -> str:
        """Повертає текстове представлення моделі."""
        return f"{self.name}"
