"""Модуль контролерів для керування налаштуваннями облікових записів."""

from django.views.generic import TemplateView


class AccountSettingsView(TemplateView):
    """Відображає сторінку налаштувань облікового запису користувача."""

    template_name: str = "account/account_settings.html"
