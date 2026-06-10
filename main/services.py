from .models import Strip
from .models import SiteConfig, Email, Phone, Social


class StripService:
    def get_all(self) -> list[Strip]:
        return Strip.objects.all()


class SiteConfigService:
    def get_all_emails(self) -> list[Email]:
        sc: SiteConfig = SiteConfig.get_solo()
        return sc.emails.all()

    def get_all_socials(self) -> list[Social]:
        sc: SiteConfig = SiteConfig.get_solo()
        return sc.socials.all()

    def get_all_phones(self) -> list[Phone]:
        sc: SiteConfig = SiteConfig.get_solo()
        return sc.phones.all()

    def get_all_emails_in_footer(self) -> list[Email]:
        return self.get_all_emails().filter(in_footer=True)

    def get_all_socials_in_footer(self) -> list[Social]:
        return self.get_all_socials().filter(in_footer=True)

    def get_all_phones_in_footer(self) -> list[Phone]:
        return self.get_all_phones().filter(in_footer=True)
