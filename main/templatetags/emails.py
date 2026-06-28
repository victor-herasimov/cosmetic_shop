from django import template
from main.models import Email
from main.services import EmailService

register = template.Library()


@register.simple_tag
def get_first_active_email() -> Email:
    return EmailService().get_first_active_email()
