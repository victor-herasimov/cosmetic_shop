"""
Модуль для головної конфігурації сайту.
"""

import os
from django.db import models
from solo.models import SingletonModel


class SiteConfig(SingletonModel):
    """
    Глобальна синглтон-модель для загальних налаштувань та контенту сайту.

    Зберігає базову інформацію, таку як назва сайту, SEO-опис, слогани для різних
    частин сторінки, а також статичні медіафайли (логотип та фавіконку).
    Оскільки це SingletonModel, у системі завжди існує лише один екземпляр цих налаштувань.
    """

    title = models.CharField(
        max_length=255,
        default="Назва сайту",
        verbose_name="Назва сайту",
        help_text="Назва сайту",
    )
    logo = models.ImageField(
        blank=True,
        null=True,
        upload_to="logo",
        verbose_name="Логотип",
        help_text="Логотип",
    )

    favicon = models.ImageField(
        blank=True,
        null=True,
        upload_to="favicon",
        verbose_name="Фавіконка",
        help_text="Фавіконка",
    )
    slogan = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        default="",
        verbose_name="Гасло",
        help_text="Слоган відображаєсться в футері",
    )
    slogan_top = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        default=None,
        verbose_name="Гасло",
        help_text="Слоган відображаєсться в на головній в заголовку.",
    )
    copyright = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        default=None,
        verbose_name="Копірайт",
        help_text="Копірайт відображаєсться в футері.",
    )
    copyright_extend = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        default=None,
        verbose_name="Додатковий копірайт",
        help_text="Додатковий копірайт відображаєсться в футері біля основного копірайта.",
    )

    contact_email = models.EmailField(
        verbose_name="Email",
        default="manage@example.com",
        help_text="Email на який будуть присилатися листи з замовленнями та іншими повідомленями",
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        """Мета-параметри для відображення глобальних налаштувань в адмін-панелі Django."""

        app_label = "main"
        verbose_name: str = "Конфігурація сайту"

    def __str__(self) -> str:
        """Повертає текстове представлення — поточну назву сайту."""
        return f"{self.title}"

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

        Перевіряє, чи змінилися файли логотипу (`logo`) або фавіконки (`favicon`),
        і якщо так — видаляє старі версії файлів з диска, щоб запобігти накопиченню сміття.
        """
        if self.pk:
            try:
                old_config = SiteConfig.objects.get(pk=self.pk)
                self._remove_media(old_config.logo, self.logo)
                self._remove_media(old_config.favicon, self.favicon)
            except SiteConfig.DoesNotExist:
                pass

        super().save(*args, **kwargs)
