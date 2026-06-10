from django import template
from main.models.email import Email
from main.models.phones import Phone
from main.models.socials import Social
from main.services import SiteConfigService

register = template.Library()


@register.simple_tag
def get_phones_in_footer() -> list[Phone]:
    scs: SiteConfigService = SiteConfigService()
    return scs.get_all_phones_in_footer()


@register.simple_tag
def get_emails_in_footer() -> list[Email]:
    scs: SiteConfigService = SiteConfigService()
    return scs.get_all_emails_in_footer()


@register.simple_tag
def get_socials_in_footer() -> list[Social]:
    scs: SiteConfigService = SiteConfigService()
    return scs.get_all_socials_in_footer()
