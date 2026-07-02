"""
Модуль фонових задач (Celery) для додатку замовлень (Order).

Забезпечує асинхронну обробку подій, пов'язаних із життєвим циклом замовлень,
зокрема рендеринг та відправку email-сповіщень клієнтам та адміністраторам
сайту після успішного оформлення покупки.

Архітектурні особливості:
    - Повністю ізольований від HTTP-шару (не приймає об'єкт HttpRequest).
    - Оптимізований для мінімізації кількості SQL-запитів до бази даних
      завдяки жадібному завантаженню даних (Eager Loading).
    - Має вбудований механізм повторних спроб (Retries) у разі тимчасових
      збоїв поштових шлюзів чи мережі.

Залежності:
    - Celery для керування чергами задач.
    - Django ORM для вибірки агрегованих даних замовлення та налаштувань сайту.
    - `notifications.services` та `notifications.handlers` для відправки листів.
"""

import logging
from typing import Any

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch

from main.models import SiteConfig
from main.services import WorkScheduleService, SiteConfigService, AddressService
from notifications.handlers import EmailNotificationHandler
from notifications.services import NotificationService
from order.models import OrderItem

from .models import Order


logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_order_notification_task(self, order_id: int, base_url: str) -> None:
    """
    Фонова задача Celery для відправки листів клієнту та менеджеру.
    """
    try:
        order: Order = (
            Order.objects.select_related("delivery_method", "payment_method")
            .prefetch_related(
                Prefetch(
                    "items",
                    queryset=OrderItem.objects.select_related(
                        "product__cateogry"
                    ).prefetch_related("product__fotos"),
                )
            )
            .get(pk=order_id)
        )
    except ObjectDoesNotExist:
        logger.error(
            "Замовлення №%s не знайдено в БД для відправки сповіщень.", order_id
        )
        return

    notifications_service: NotificationService = NotificationService(
        handlers=[EmailNotificationHandler()]
    )
    schedules: list[str] = [str(item) for item in WorkScheduleService.get_all()]
    config: SiteConfig = SiteConfigService().get()
    address_service: AddressService = AddressService()

    context: dict[str, Any] = {
        "config": config,
        "order": order,
        "base_url": base_url,
        "schedule": ", ".join(schedules),
        "phones": config.phones.all(),
        "emails": config.emails.all(),
        "socials": config.socials.all(),
        "addresses": address_service.get_all(),
    }
    # TODO add admin from db
    try:
        # Відправка клієнту
        notifications_service.notify(
            template_name_text="order/emails/email-order-confirmation.txt",
            context=context,
            template_name_html="order/emails/email-order-confirmation.html",
            email=order.email,
            subject=f"Замовлення №{ order.id } підтверджено!",
        )
        # Відправка менеджеру
        notifications_service.notify(
            template_name_text="order/emails/email-admin-order.txt",
            context=context,
            template_name_html="order/emails/email-admin-order.html",
            email="admin@mybeauty.com",
            subject=f"НОВЕ ЗАМОВЛЕННЯ №{order.id} — {order.get_total_cost()} грн — {order.last_name}",
        )
    except Exception as exc:
        logger.warning(
            "Помилка відправки листів для замовлення %s. Повторна спроба...", order_id
        )
        raise self.retry(exc=exc)
