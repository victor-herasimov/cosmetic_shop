from django import template
from main.services import StripService

register = template.Library()


@register.simple_tag
def get_strips():
    strip_servise: StripService = StripService()
    return strip_servise.get_all()
