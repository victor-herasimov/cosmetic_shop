from django.contrib import admin
from feedback.models import Feedback


@admin.register(Feedback)
class FeedbackReadOnlyAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "subject"]
    fields = ["name", "phone", "email", "subject", "body"]

    def has_add_permission(self, request):
        return False
