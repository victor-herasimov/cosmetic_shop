"""
Модуль налаштування панелі адміністратора Django для додатку товарів (goods).

Цей файл містить конфігурацію відображення моделей Product, Foto, Characteristic
та CharacteristicItem в адмін-панелі, включаючи кастомні інлайни (inlines)
та групування полів (fieldsets).
"""

from django.contrib import admin
from django.utils.safestring import mark_safe

from goods.models import Product
from goods.models import Foto
from goods.models import Characteristic
from goods.models.characteristic_item import CharacteristicItem

from .actions import duplicate_product_action


@admin.register(CharacteristicItem)
class OtherCharacteristicItemAdmin(admin.ModelAdmin):
    """
    Налаштування адмін-панелі для моделі назв характеристик (напр., 'Колір', 'Об'єм').
    """

    list_display = ["name"]
    list_display_links = ["name"]
    fields = ["name"]


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    """
    Налаштування адмін-панелі для конкретних значень характеристик.
    Поєднує назву характеристики (item) та її значення (value).
    """

    list_display = ["item", "value"]
    list_display_links = ["item", "value"]
    fields = ["item", "value"]


class CharacteristicInline(admin.TabularInline):
    """
    Вбудоване (Inline) відображення характеристик безпосередньо в картці товару.
    Використовує проміжну таблицю ManyToMany зв'язку.
    """

    model = Product.characteristics.through
    # fields = ["value"]
    extra = 0


class FotoInline(admin.TabularInline):
    """
    Вбудоване (Inline) відображення галереї зображень товару в картці товару.
    Дозволяє завантажувати фото та обирати головне зображення.
    """

    model = Foto

    def thumbnail(self, obj):
        """Генерує HTML-тег для відображення мініатюри завантаженого зображення."""

        return mark_safe(f'<img src="{obj.image.url}" width="95"') if obj.image else "-"

    thumbnail.short_description = "Мініатюрка"
    fields = ["thumbnail", "image", "is_main"]
    readonly_fields = ["thumbnail"]
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Основне налаштування адмін-панелі для моделі товару (Product).

    Включає:
    - Кастомну дію дублювання товару (duplicate_product_action).
    - Фільтрацію за категоріями.
    - Вбудовані блоки (inlines) для фото та характеристик.
    - Структуроване групування полів (fieldsets) для зручного редагування інформації.
    - Автоматичну генерацію slug на основі назви (title).
    """

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
            {"fields": ["id", "title", "slug", "cateogry", "is_bestseller", "is_new"]},
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
        ("Переваги", {"fields": ["vegan_frendly", "derma", "delivery", "active"]}),
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
