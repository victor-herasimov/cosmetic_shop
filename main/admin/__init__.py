from django.contrib import admin
from .hero import HeroAdmin
from .site_config import SiteConfigAdmin
from .strip import StripAdmin


admin.site.site_header = "Адміністрування магазину"
admin.site.site_title = "Адміністрування магазину"

__all__ = ["HeroAdmin", "SiteConfigAdmin", "StripAdmin"]
