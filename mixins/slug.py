from django.db import models


class SlugMixin(models.Model):
    slug = models.SlugField(max_length=256, verbose_name="Слаг")

    class Meta:
        abstract = True
