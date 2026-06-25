"""
Базовий клас та абстрактна модель юридичних документів сайту.

Цей модуль визначає загальну структуру, поля та логіку для офіційних сторінок
(таких як Правила користування, Політика конфідеційності тощо), мінімізуючи
дублювання коду за допомогою абстрактних класів та міксинів.
"""

from django.db import models
from solo.models import SingletonModel
from django_ckeditor_5.fields import CKEditor5Field
from mixins import DateMixin


class BaseLegalDocument(SingletonModel, DateMixin):
    """
    Абстрактна синглтон-модель для юридичних та офіційних документів сайту.

    Служить базовим класом для документів, які мають існувати в системі
    в єдиному екземплярі (наприклад, Політика конфідеційності, Публічна оферта).
    Поєднує функціонал єдиного запису (SingletonModel), автоматичне логування
    дат створення/оновлення (DateMixin) та підтримку форматованого тексту (CKEditor5).
    """

    title = models.CharField(max_length=256, verbose_name="Заголовок")
    content = CKEditor5Field(
        "Текст документа",
        config_name="extends",
        blank=True,
        null=True,
        default=None,
    )

    class Meta:
        """Мета-параметри для визначення абстрактного характеру моделі."""

        abstract = True
