from django.contrib import admin
from django.utils.safestring import mark_safe

from goods.models import Product
from goods.models import Foto
from goods.models import Characteristic
from goods.models.characteristic_item import CharacteristicItem

from .actions import duplicate_product_action


@admin.register(CharacteristicItem)
class OtherCharacteristicItemAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]
    fields = ["name"]


@admin.register(Characteristic)
class OtherCharacteristicAdmin(admin.ModelAdmin):
    list_display = ["item", "value"]
    list_display_links = ["item", "value"]
    fields = ["item", "value"]


class CharacteristicInline(admin.TabularInline):
    model = Product.characteristics.through
    # fields = ["value"]
    extra = 0


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
    actions = [duplicate_product_action]
    save_as = False
    save_on_top = True
    list_display = ["id", "title"]
    list_display_links = ["id", "title"]
    list_filter = [
        "cateogry",
    ]
    inlines = [FotoInline, CharacteristicInline]
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
        ("Склад", {"fields": ["composition"]}),
        (
            "Опис",
            {"fields": ["description"]},
        ),
        ("Спосіб застосування", {"fields": ["method_apply"]}),
        ("Дати", {"fields": ["created", "updated"]}),
    ]
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ["id", "created", "updated"]
