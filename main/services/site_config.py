from django.db.models import QuerySet
from main.models import SiteConfig, Email, Phone, Social


class SiteConfigService:
    def get_all_emails(self) -> list[Email]:
        sc: SiteConfig = SiteConfig.objects.prefetch_related("emails").get()
        print(type(sc))
        return sc.emails.all()

    def get_all_socials(self) -> QuerySet[Social]:
        sc: SiteConfig = SiteConfig.objects.prefetch_related("socials").get()
        return sc.socials.all()

    def get_all_phones(self) -> QuerySet[Phone]:
        sc: SiteConfig = SiteConfig.objects.prefetch_related("phones").get()
        return sc.phones.all()

    def get_all_emails_in_footer(self) -> QuerySet[Email]:
        return self.get_all_emails().filter(in_footer=True)

    def get_all_socials_in_footer(self) -> QuerySet[Social]:
        return self.get_all_socials().filter(in_footer=True)

    def get_all_phones_in_footer(self) -> QuerySet[Phone]:
        return self.get_all_phones().filter(in_footer=True)
