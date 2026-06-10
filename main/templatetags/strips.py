from django import template
from main.servises import StripServise

register = template.Library()


@register.simple_tag
def get_strips():
    strip_servise: StripServise = StripServise()
    return strip_servise.get_all()
