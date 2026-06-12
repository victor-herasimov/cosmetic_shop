from django.db.models import QuerySet
from main.models import SiteConfig, Email, Phone, Social


class SiteConfigService:
    def get(self) -> SiteConfig:
        """
        Повертає конфігурацію сайта.
        """
        return SiteConfig.objects.prefetch_related("emails", "socials", "phones")
