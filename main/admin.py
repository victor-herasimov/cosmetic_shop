from django.contrib import admin
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin
from .models import SiteConfig, Strip, Hero, Email, Phone, Social


class EmailInline(admin.TabularInline):
    model = Email
    extra = 0


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0


class SocialInline(admin.TabularInline):
    model = Social
    extra = 0


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
    inlines = [EmailInline, PhoneInline, SocialInline]


@admin.register(Strip)
class StripAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]
    fields = ["name", "created", "updated"]

    readonly_fields = ["created", "updated"]


@admin.register(Hero)
class HeroAdmin(SingletonModelAdmin):
    def thumbnail(self, obj):

        return (
            mark_safe(f'<img src="{obj.image.url}" width="60" height="60"')
            if obj.image
            else "-"
        )

    thumbnail.short_description = "Мініатюрка"

    list_display = ["title", "subtitle"]
    list_display_links = ["title", "subtitle"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "subtitle",
                    "short_description",
                    "badge_title",
                    "badge_value",
                ]
            },
        ),
        ("Картинка", {"fields": ["thumbnail", "image"]}),
    ]
    readonly_fields = ["created", "updated", "thumbnail"]
