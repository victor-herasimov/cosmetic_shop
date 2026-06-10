from django.contrib import admin
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin
from main.models import SiteConfig, Email, Phone, Social


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
