from django.db import models
from . import SiteConfig


class Social(models.Model):
    title = models.EmailField(verbose_name="Соціальна мережа")
    url = models.URLField(max_length=255, verbose_name="URL")
    in_footer = models.BooleanField(default=True, verbose_name="Показувати в футері")
    active = models.BooleanField(default=True, verbose_name="Активний")

    config = models.ForeignKey(
        SiteConfig,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="socials",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        app_label = "main"
        verbose_name = "Соціальна мережа"
        verbose_name_plural = "Соціальні мережі"
