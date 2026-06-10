from django.contrib import admin
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin
from main.models import Hero


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
