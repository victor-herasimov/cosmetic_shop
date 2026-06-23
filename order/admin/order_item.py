from django.contrib import admin
from order.models import OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem

    def get_cost(self, obj):
        if not obj.id is None:
            return f"{obj.get_cost()}"
        else:
            print("Object none")
            return "-"

    get_cost.short_description = "Вартість: "

    fields = ["product", "price", "quantity", "get_cost"]
    readonly_fields = ["get_cost", "price"]
    extra = 0
