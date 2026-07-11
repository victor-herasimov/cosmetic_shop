import logging

from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import AbstractUser

from main.models import SiteConfig
from main.services import SiteConfigService, AddressService, WorkScheduleService
from notifications.handlers.email import EmailNotificationHandler
from notifications.services import NotificationService

User: type[AbstractUser] = get_user_model()
logger = logging.getLogger(__name__)

from celery.utils.log import get_task_logger

celery_logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_reset_email_task(
    self,
    user_id: int,
    domain: str,
    protocol: str,
    template_name_email_text: str,
    template_name_email_html: str,
    base_url: str,
) -> None:
    user: AbstractUser = User.objects.get(pk=user_id)

    uid: str = urlsafe_base64_encode(force_bytes(user.pk))
    token: str = default_token_generator.make_token(user)

    celery_logger.info(uid)
    celery_logger.info(token)

    config: SiteConfig = SiteConfigService().get()
    schedules: list[str] = [str(item) for item in WorkScheduleService.get_all()]
    config: SiteConfig = SiteConfigService().get()
    address_service: AddressService = AddressService()

    context = {
        "first_name": user.first_name,
        "domain": domain,
        "site_name": domain,
        "uidb64": uid,
        "token": token,
        "protocol": protocol,
        "config": config,
        "base_url": base_url,
        "schedule": ", ".join(schedules),
        "phones": config.phones.all(),
        "emails": config.emails.all(),
        "socials": config.socials.all(),
        "addresses": address_service.get_all(),
    }

    notifications_service: NotificationService = NotificationService(
        handlers=[EmailNotificationHandler()]
    )

    try:
        notifications_service.notify(
            template_name_text=template_name_email_text,
            context=context,
            template_name_html=template_name_email_html,
            email=user.email,
            subject=f"Відновлення пароля до вашого акаунту {config.title}",
        )
    except Exception as exc:
        logger.warning(
            "Помилка відправки листів для користувача %s. Повторна спроба...",
            user.email,
        )
        raise self.retry(exc=exc)
