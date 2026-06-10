from django.contrib import admin
from main.models import Strip


@admin.register(Strip)
class StripAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]
    fields = ["name", "created", "updated"]

    readonly_fields = ["created", "updated"]
