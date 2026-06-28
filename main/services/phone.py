from main.models import Phone


class PhoneService:
    @classmethod
    def get_first_active_phone(cls) -> Phone | None:
        """
        Повертає перший активний телефон.
        """
        return Phone.objects.filter(active=True).first()
