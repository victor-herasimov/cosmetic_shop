from main.models.site_config import SiteConfig

from .services import SiteConfigService


def site_settings(request) -> dict[str, SiteConfig | None]:
    config: SiteConfig | None = SiteConfigService().get()

    if config:
        return {
            "site_config": config,
            "emails": config.emails.all(),
            "phones": config.phones.all(),
            "socials": config.socials.all(),
        }
    return {"site_config": None, "emails": [], "phones": [], "socials:": []}
