from django.apps import AppConfig


class GoodsConfig(AppConfig):
    name = "goods"
    verbose_name = "Укравління товарами"

    def ready(self):
        from . import signals
