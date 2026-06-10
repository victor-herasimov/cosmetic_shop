from django.db import models
from . import SiteConfig


class Email(models.Model):
    email = models.EmailField(verbose_name="Email")
    in_footer = models.BooleanField(default=True, verbose_name="Показувати в футері")
    active = models.BooleanField(default=True, verbose_name="Активний")

    config = models.ForeignKey(
        SiteConfig,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="emails",
    )

    def __str__(self):
        return f"{self.email}"

    class Meta:
        app_label = "main"
        verbose_name = "Email"
        verbose_name_plural = "Emails"
