from django.db import models


class CharacteristicItem(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва характеристики")

    class Meta:
        ordering = ["name"]
        verbose_name = "Назву характеристики"
        verbose_name_plural = "Назви характеристик"

    def __str__(self):
        return f"{self.name}"
