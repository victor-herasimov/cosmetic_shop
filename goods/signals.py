import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Foto


@receiver(post_delete, sender=Foto)
def delete_image_on_delete(sender, instance, **kwargs) -> None:
    """
    Видаляє фотографію з диска, якщо запис видаляється.
    """
    # Перевіряємо, чи існує поле з фото та чи є у нього файл
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
