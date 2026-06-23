from django.contrib import admin
from order.models import DeliveryMethod


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active"]
    list_display_links = ["title"]

    fields = ["title", "is_active", "short_description"]
    readonly_fields = ["id"]
