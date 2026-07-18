from django.views.generic import TemplateView


class UserOrderList(TemplateView):
    template_name = "account/orders.html"
    extra_context = {"elided_page_range": ["1", "2", "...", "10", "...", "45", "46"]}
