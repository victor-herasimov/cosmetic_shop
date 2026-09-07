from .base import *

DEBUG = False


STATIC_ROOT: Path = BASE_DIR / "static_prod"

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# Базове налаштування для продакшну (1 рік)
# SECURE_HSTS_SECONDS = 31536000

# Рекомендовано включити додаткові прапорці безпеки:
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Застосовувати HSTS до всіх піддоменів
# SECURE_HSTS_PRELOAD = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")


INSTALLED_APPS: list[str] = INTERNAL_APPS + OUTHER_APPS + CREATED_APPS


# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST: str | None = os.environ.get("EMAIL_HOST")
EMAIL_PORT: str | None = os.environ.get("EMAIL_PORT")
DEFAULT_FROM_EMAIL: str | None = os.environ.get("DEFAULT_FROM_EMAIL")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = read_secret("email_host_pass") or os.environ.get(
    "EMAIL_HOST_PASSWORD"
)
EMAIL_USE_TLS = bool(int(os.environ.get("EMAIL_USE_TLS")))
EMAIL_USE_SSL = bool(int(os.environ.get("EMAIL_USE_SSL")))
