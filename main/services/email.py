from main.models import Email


class EmailService:
    @classmethod
    def get_first_active_email(cls) -> Email | None:
        """
        Повертає перший активний email.
        """
        return Email.objects.filter(active=True).first()
