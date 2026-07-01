"""Модуль ініціалізації та конфігурації Celery для проєкту Django.

Цей модуль налаштовує екземпляр додатка Celery, пов'язуючи його з
налаштуваннями Django, та автоматично шукає асинхронні завдання (tasks)
у всіх зареєстрованих додатках проєкту.
"""

import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
app: Celery = Celery("shop")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
