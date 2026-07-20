"""
Модуль налаштування адміністративної панелі Django для додатку goods.
"""

from django.contrib import admin
from goods.models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    Налаштування відображення та керування моделлю Brand в адмін-панелі.
    """

    list_display = ("name", "slug", "created", "updated")
    search_fields = ("name", "slug")
    list_filter = ("created", "updated")
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 20
