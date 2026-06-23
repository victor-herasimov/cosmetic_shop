from main.models import SiteConfig


class SiteConfigService:
    def get(self) -> SiteConfig:
        """
        Повертає конфігурацію сайта.
        """
        return SiteConfig.objects.prefetch_related("emails", "socials", "phones")
