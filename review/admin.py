from django.contrib import admin

from review.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "user", "rating", "short_text")
    list_display_links = ("id", "product")
    list_filter = ("rating",)
    search_fields = ("user__email", "text", "product__title")
    raw_id_fields = ("product", "user")  # Оптимізація вибору для великих баз даних

    @admin.display(description="Текст відгуку")
    def short_text(self, obj: Review) -> str:
        if len(obj.text) > 50:
            return f"{obj.text[:50]}..."
        return obj.text
