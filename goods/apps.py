from django.apps import AppConfig


class GoodsConfig(AppConfig):
    name = "goods"
    verbose_name = "Укравління прдуктами"

    def ready(self):
        from . import signals
