"""Модуль управлінням конфігурацією сайту."""

from django.db.models import Prefetch, QuerySet
from main.models import SiteConfig, Email, Phone, Social


class SiteConfigService:
    """Сервіс управлінням конфігурацією сайту."""

    def get(self) -> SiteConfig | None:
        """
        Повертає конфігурацію сайта.
        """
        active_emails: QuerySet[Email] = Email.objects.filter(active=True)
        active_phones: QuerySet[Phone] = Phone.objects.filter(active=True)
        active_socials: QuerySet[Social] = Social.objects.filter(active=True)

        site_config: SiteConfig | None = SiteConfig.objects.prefetch_related(
            Prefetch("emails", queryset=active_emails),
            Prefetch("socials", queryset=active_socials),
            Prefetch("phones", queryset=active_phones),
        ).first()
        if not site_config:
            return SiteConfig.get_solo()

        return site_config
