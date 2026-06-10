import re
from django.db import models

from . import SiteConfig
from main.validators import PhoneNumberValidator


class Phone(models.Model):
    phone = models.CharField(
        max_length=17, verbose_name="Телефон", validators=[PhoneNumberValidator()]
    )
    in_footer = models.BooleanField(default=True, verbose_name="Показувати в футері")
    active = models.BooleanField(default=True, verbose_name="Активний")

    config = models.ForeignKey(
        SiteConfig,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="phones",
    )

    def __str__(self):
        return f"{self.phone}"

    def clean_number(self):
        return re.sub(r"[/(/)/-]", "", self.phone)

    class Meta:
        app_label = "main"
        verbose_name = "Телефон"
        verbose_name_plural = "Телефони"
