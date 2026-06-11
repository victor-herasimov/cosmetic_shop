from django.contrib import admin
from django.utils.safestring import mark_safe

from goods.models import Product
from goods.models import Foto


class FotoInline(admin.TabularInline):
    model = Foto

    def thumbnail(self, obj):

        return mark_safe(f'<img src="{obj.image.url}" width="95"') if obj.image else "-"

    thumbnail.short_description = "Мініатюрка"
    fields = ["thumbnail", "image", "is_main"]
    readonly_fields = ["thumbnail"]
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ["id", "title"]
    list_display_links = ["id", "title"]
    list_filter = [
        "cateogry",
    ]
    inlines = [FotoInline]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "id",
                    "title",
                    "slug",
                    "cateogry",
                ]
            },
        ),
        (
            "Ціна - Залишки",
            {
                "fields": [
                    (
                        "price",
                        "discount",
                    ),
                    "count",
                ]
            },
        ),
        (
            "Опис",
            {"fields": ["description"]},
        ),
        ("Дати", {"fields": ["created", "updated"]}),
    ]
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ["id", "created", "updated"]
