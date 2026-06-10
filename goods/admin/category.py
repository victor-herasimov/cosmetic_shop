from django.contrib import admin
from goods.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "updated", "created"]
    list_display_links = ["name"]
    # fields = ["name", "slug", "short_description", "updated", "created"]
    fieldsets = [
        (None, {"fields": ["name", "slug", "short_description", "visible"]}),
        ("Дати", {"fields": ["updated", "created"]}),
    ]
    prepopulated_fields = {"slug": ["name"]}
    readonly_fields = ["updated", "created"]
