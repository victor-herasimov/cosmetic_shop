from .services import SiteConfigService


def site_settings(request):
    return {"site_config": SiteConfigService().get()}
