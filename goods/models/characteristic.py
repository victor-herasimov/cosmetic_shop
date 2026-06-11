from django.db import models
from .characteristic_item import CharacteristicItem


class Characteristic(models.Model):
    item = models.ForeignKey(
        CharacteristicItem,
        on_delete=models.CASCADE,
        verbose_name="Характеристика",
        related_name="items",
    )
    value = models.CharField(max_length=64, verbose_name="Значення характеристики")

    class Meta:
        ordering = ["item"]
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"
        constraints = [
            models.UniqueConstraint(fields=("item", "value"), name="unique_item_value")
        ]

    def __str__(self):
        return f"{self.item} - {self.value}"
