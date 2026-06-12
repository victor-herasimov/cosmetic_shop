from django import template

register = template.Library()


@register.filter
def uk_pluralize(n: int) -> str:
    mod_10: int = n % 10
    mod_100: int = n % 100
    if mod_10 == 1 and mod_100 != 11:
        return "товар"
    if mod_10 >= 2 and mod_10 <= 4 and (mod_100 < 10 or mod_100 >= 20):
        return "товари"
    return "товарів"
