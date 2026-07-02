"""
Модуль для інтеграції та налаштування панелі адміністратора моделі `SEOPage`.

Забезпечує зручний та структурований інтерфейс (UI) для керування SEO-налаштуваннями
статичних сторінок. Налаштовує логічне групування полів (fieldsets), фільтрацію,
пошук, а також додає візуальний попередній перегляд (прев'ю) завантажених
Open Graph зображень безпосередньо в списку об'єктів та на сторінці редагування.
"""

from django.contrib import admin
from django.utils.safestring import mark_safe
from seo.models import SEOPage


@admin.register(SEOPage)
class SEOPageAdmin(admin.ModelAdmin):
    """
    Конфігурація панелі адміністратора для моделі SEOPage.

    Групує поля для зручності заповнення мета-даних та забезпечує
    попередній перегляд завантажених OG-зображень.
    """

    # Налаштування відображення списку об'єктів
    list_display = ("page_type_display", "title", "get_preview_image")
    list_filter = ("page_type",)
    search_fields = ("title", "description", "keywords")
    ordering = ("page_type",)
    save_on_top = True

    # Структуризація форми редагування за допомогою fieldsets
    fieldsets = (
        (
            "Основні налаштування",
            {
                "fields": ("page_type", "title"),
                "description": "Виберіть цільову сторінку та вкажіть головний заголовок.",
            },
        ),
        (
            "Мета-описи та ключові слова",
            {
                "fields": ("description", "keywords"),
                "classes": ("collapse",),  # Можна згорнути за потреби
                "description": "Ці дані використовуються пошуковими роботами для індексації.",
            },
        ),
        (
            "Соціальні мережі (Open Graph)",
            {
                "fields": ("image", "preview_image_field"),
                "description": "Зображення, яке відображатиметься при поширенні посилання у соцмережах.",
            },
        ),
    )

    # Дозволяє вивести кастомне поле для прев'ю у формі редагування
    readonly_fields = ("preview_image_field",)

    @admin.display(description="Сторінка сайту")
    def page_type_display(self, obj: SEOPage) -> str:
        """Відображає зрозумілу назву сторінки замість її URL-шляху."""
        return obj.get_page_type_display()

    @admin.display(description="Прев'ю OG Image")
    def get_preview_image(self, obj: SEOPage) -> str:
        """Генерує мініатюру зображення для списку всіх записів."""
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height: 40px; border-radius: 4px;" />'
            )
        return mark_safe('<span style="color: #999;">Немає зображення</span>')

    @admin.display(description="Поточне зображення")
    def preview_image_field(self, obj: SEOPage) -> str:
        """Генерує велике прев\'ю зображення для форми редагування сторінки."""
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height: 200px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />'
            )
        return mark_safe(
            '<span style="color: #999;">Зображення ще не завантажено</span>'
        )
