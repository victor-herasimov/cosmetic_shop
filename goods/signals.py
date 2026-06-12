import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Foto


@receiver(post_delete, sender=Foto)
def delete_image_on_delete(sender, instance, **kwargs) -> None:
    """
    Видаляє фотографію з диска, якщо запис видаляється.
    """
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(post_save, sender=Foto)
def set_only_one_main_foto(sender, instance, **kwargs) -> None:
    """
    Встановлює тільки одну фотографію головною.
    """
    if instance.is_main:
        Foto.objects.filter(product=instance.product).exclude(pk=instance.pk).update(
            is_main=False
        )
