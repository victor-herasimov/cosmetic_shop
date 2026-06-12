import os
from django.db import models
from solo.models import SingletonModel


class SiteConfig(SingletonModel):
    title = models.CharField(
        max_length=255,
        default="Назва сайту",
        verbose_name="Назва сайту",
        help_text="Назва сайту",
    )
    short_description = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        default=None,
        verbose_name="Короткий опис",
        help_text="Короткий опис для SEO",
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
        default=None,
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

    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        app_label = "main"
        verbose_name: str = "Конфігурація сайту"

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_config = SiteConfig.objects.get(pk=self.pk)
                if old_config.logo and old_config.logo != self.logo:
                    if os.path.isfile(old_config.logo.path):
                        os.remove(old_config.logo.path)
                if old_config.favicon and old_config.favicon != self.favicon:
                    if os.path.isfile(old_config.favicon.path):
                        os.remove(old_config.favicon.path)
            except SiteConfig.DoesNotExist:
                pass

        super().save(*args, **kwargs)
