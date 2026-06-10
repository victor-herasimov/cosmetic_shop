import os
from django.db import models
from solo.models import SingletonModel


class SiteConfig(SingletonModel):
    title = models.CharField(
        max_length=255, default="Назва сайту", verbose_name="Назва сайту"
    )
    short_description = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        default=None,
        verbose_name="Короткий опис",
    )
    logo = models.ImageField(
        blank=True, null=True, upload_to="logo", verbose_name="Логотип"
    )
    slogan = models.CharField(
        max_length=512, null=True, blank=True, default=None, verbose_name="Гасло"
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
            except SiteConfig.DoesNotExist:
                pass

        super().save(*args, **kwargs)
