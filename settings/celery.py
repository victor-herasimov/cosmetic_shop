"""Модуль ініціалізації та конфігурації Celery для проєкту Django.

Цей модуль налаштовує екземпляр додатка Celery, пов'язуючи його з
налаштуваннями Django, та автоматично шукає асинхронні завдання (tasks)
у всіх зареєстрованих додатках проєкту.
"""

from celery import Celery


app: Celery = Celery("shop")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
