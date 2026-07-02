"""
Модуль для керування SEO-налаштуваннями статичних сторінок сайту.

Містить модель `SEOPage`, яка інтегрується з пакетом `django-meta` для динамічного
формування мета-тегів (title, description, keywords, Open Graph) для головних
та статичних розділів веб-ресурсу.
"""

import os

from django.db import models
from meta.models import ModelMeta


class SEOPage(ModelMeta, models.Model):
    """
    Модель для збереження та керування SEO-даними конкретних статичних сторінок.

    Дозволяє адміністраторам сайту через панель керування задавати унікальні
    заголовки, описи, ключові слова та зображення (OG Image) для кожної сторінки,
    що реалізована в системі. Наслідує `ModelMeta` для автоматизації генерації тегів.
    """

    class PageChoices(models.TextChoices):
        """
        Перелік підтримуваних сторінок сайту для налаштування SEO.

        Значення (value) вказує на відносний шлях (URL) сторінки,
        а мітка (label) — на її зрозумілу назву для адміністратора.
        """

        MAIN = ("/", "Головна сторінка")
        CATALOG = ("/catalog/", "Каталог")
        CONTACT = ("/pages/contact/", "Контакти")

    page_type = models.CharField(
        max_length=100,
        choices=PageChoices,
        unique=True,
        verbose_name="Сторінка сайту",
        help_text="Виберіть сторінку, до якої хочете налаштувати SEO",
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок (Title)")
    description = models.TextField(verbose_name="Опис (Description)", blank=True)
    keywords = models.CharField(
        max_length=255,
        verbose_name="Ключові слова",
        blank=True,
        help_text="Введіть ключові слова через кому",
    )
    image = models.ImageField(
        upload_to="seo_images/", verbose_name="OG Зображення", blank=True, null=True
    )

    _metadata: dict[str, str] = {
        "title": "title",
        "description": "description",
        "keywords": "get_keywords_list",
        "image": "get_image_url",
        "og_type": "website",
    }

    class Meta:
        verbose_name = "SEO для статичної сторінки"
        verbose_name_plural = "SEO для статичних сторінок"

    def __str__(self) -> str:
        """
        Повертає текстове представлення об'єкта (назву сторінки з PageChoices).
        """
        return self.get_page_type_display()

    def get_keywords_list(self) -> list[str]:
        """
        Перетворює рядок ключових слів, розділених комами, у список.

        Попередньо очищає кожен елемент від зайвих пробілів на початку та в кінці.

        Returns:
            list[str]: Список ключових слів або порожній список, якщо поле пусте.
        """
        return [k.strip() for k in self.keywords.split(",")] if self.keywords else []

    def get_image_url(self) -> str | None:
        """
        Повертає URL завантаженого зображення для мета-тегів.

        Returns:
            str | None: Шлях до файлу зображення або None, якщо зображення відсутнє.
        """
        return self.image.url if self.image else None

    def _remove_media(
        self, old_file: models.FieldFile, new_file: models.FieldFile
    ) -> None:
        """
        Допоміжний метод для видалення старого медіафайлу з диска.
        """
        if old_file and old_file != new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

    def save(self, *args, **kwargs) -> None:
        """
        Зберігає конфігурацію та автоматично видаляє застарілі файли.

        Перевіряє, чи змінилися файли зображення,
        і якщо так — видаляє старі версії файлів з диска, щоб запобігти накопиченню сміття.
        """
        if self.pk:
            try:
                old_seo_page = SEOPage.objects.get(pk=self.pk)
                self._remove_media(old_seo_page.image, self.image)
            except SEOPage.DoesNotExist:
                pass

        super().save(*args, **kwargs)
