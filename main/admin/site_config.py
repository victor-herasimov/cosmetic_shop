from django.contrib import admin
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin
from main.models import SiteConfig, Email, Phone, Social, Address, WorkSchedule


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0


class WorkScheduleInline(admin.TabularInline):
    model = WorkSchedule
    extra = 0


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

    def thumbnail_favicon(self, obj):

        return (
            mark_safe(f'<img src="{obj.favicon.url}" width="40"')
            if obj.favicon
            else "-"
        )

    thumbnail_favicon.short_description = "Мініатюрка фавіконки"

    list_display = ["title", "short_description"]
    list_display_links = ["title"]
    fieldsets = [
        (None, {"fields": ["title", "short_description", "slogan_top", "slogan"]}),
        ("Логотип", {"fields": ["thumbnail", "logo"]}),
        ("Фавіконка", {"fields": ["thumbnail_favicon", "favicon"]}),
    ]
    readonly_fields = ["created", "updated", "thumbnail", "thumbnail_favicon"]
    inlines = [
        EmailInline,
        PhoneInline,
        SocialInline,
        AddressInline,
        WorkScheduleInline,
    ]
