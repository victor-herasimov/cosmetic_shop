from django.contrib import admin
from pathlib import Path
from django.core.files.base import ContentFile


@admin.action(description="Копіювати продукт з усіма даними")
def duplicate_product_action(modeladmin, request, queryset) -> None:
    for product in queryset:
        characteristics = list(product.characteristics.all())
        photos = list(product.fotos.all())

        product.pk = None
        product.id = None
        product.save()

        product.characteristics.set(characteristics)

        for photo in photos:
            if photo.image:
                old_image = photo.image
                new_image_content = ContentFile(old_image.read())

                photo.pk = None
                photo.id = None
                photo.product = product
                old_file_name = Path(old_image.name).name
                photo.image.save(old_file_name, new_image_content, save=False)
            else:
                photo.pk = None
                photo.id = None
                photo.product = product
            photo.save()
