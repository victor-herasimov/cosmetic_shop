from django import template
from main.models import Phone
from main.services import PhoneService

register = template.Library()


@register.simple_tag
def get_first_active_phone() -> Phone:
    return PhoneService.get_first_active_phone()
