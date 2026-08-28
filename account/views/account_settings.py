"""Модуль контролерів для керування налаштуваннями облікових записів."""

from django.views.generic import TemplateView
from view_breadcrumbs import BaseBreadcrumbMixin

from mixins import HTMXLoginRequiredMixin


class AccountSettingsView(BaseBreadcrumbMixin, HTMXLoginRequiredMixin, TemplateView):
    """Відображає сторінку налаштувань облікового запису користувача."""

    template_name: str = "account/account_settings.html"

    crumbs = [
        ("Налаштування", ""),
    ]
