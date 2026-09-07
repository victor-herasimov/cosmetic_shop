import socket

from .base import *

DEBUG = True


ALLOWED_HOSTS = ["*"]


OUTHER_APPS: list[str] = ["debug_toolbar", *OUTHER_APPS]


INSTALLED_APPS: list[str] = INTERNAL_APPS + OUTHER_APPS + CREATED_APPS


MIDDLEWARE: list[str] = ["debug_toolbar.middleware.DebugToolbarMiddleware", *MIDDLEWARE]


hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "192.168.0.166"]


# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST: str | None = os.environ.get("EMAIL_HOST")
EMAIL_PORT: str | None = os.environ.get("EMAIL_PORT")
DEFAULT_FROM_EMAIL: str | None = os.environ.get("DEFAULT_FROM_EMAIL")
EMAIL_USE_TLS = bool(int(os.environ.get("EMAIL_USE_TLS")))
EMAIL_USE_SSL = bool(int(os.environ.get("EMAIL_USE_SSL")))
