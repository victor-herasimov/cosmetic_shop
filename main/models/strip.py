from django.db import models


class Strip(models.Model):
    name = models.CharField(max_length=255, verbose_name="Елемент")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        app_label = "main"
        verbose_name: str = "Стрічку"
        verbose_name_plural: str = "Стрічки"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"
