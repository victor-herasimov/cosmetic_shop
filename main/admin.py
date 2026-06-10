from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import SiteConfig


# admin.site.register(SiteConfig, SingletonModelAdmin)


@admin.register(SiteConfig)
class SiteConfigAdmin(SingletonModelAdmin):
    list_display = ["title", "short_description"]
    list_display_links = ["title"]
    fields = ["title", "short_description", "slogan", "logo"]
    readonly_fields = ["created", "updated"]
