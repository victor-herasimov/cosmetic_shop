from django.contrib import admin
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin
from .models import SiteConfig, Strip


@admin.register(SiteConfig)
class SiteConfigAdmin(SingletonModelAdmin):
    def thumbnail(self, obj):

        return mark_safe(f'<img src="{obj.logo.url}" width="145"') if obj.logo else "-"

    thumbnail.short_description = "Мініатюрка"

    list_display = ["title", "short_description"]
    list_display_links = ["title"]
    fieldsets = [
        (None, {"fields": ["title", "short_description", "slogan"]}),
        ("Логотип", {"fields": ["thumbnail", "logo"]}),
    ]
    readonly_fields = ["created", "updated", "thumbnail"]


@admin.register(Strip)
class StripAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]
    fields = ["name", "created", "updated"]

    readonly_fields = ["created", "updated"]
