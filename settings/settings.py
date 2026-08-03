import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv


load_dotenv()

BASE_DIR: Path = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = os.environ.get(
    "SECRET_KEY", "django-insecure-=qj+x7kug7uv&97u=3h0^#rjv7!d9zlt12(-wjq_v&2xiy2i!%"
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = bool(int(os.environ.get("DEBUG", 1)))

ALLOWED_HOSTS: list[str] = ["*"]


# Application definition
INTERNAL_APPS: list[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

OUTHER_APPS: list[str] = [
    "solo",
    "django_ckeditor_5",
    "debug_toolbar",
    "meta",
]

CREATED_APPS: list[str] = [
    "main.apps.MainConfig",
    "goods.apps.GoodsConfig",
    "cart.apps.CartConfig",
    "order.apps.OrderConfig",
    "pages.apps.PagesConfig",
    "feedback.apps.FeedbackConfig",
    "notifications.apps.NotificationsConfig",
    "seo.apps.SeoConfig",
    "account.apps.AccountConfig",
    "wishlist.apps.WishlistConfig",
]

INSTALLED_APPS: list[str] = INTERNAL_APPS + OUTHER_APPS + CREATED_APPS

MIDDLEWARE: list[str] = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "account.backends.EmailOrPhoneBackend",
]

ROOT_URLCONF: str = "settings.urls"

TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "goods.context_processors.all_categories",
                "goods.context_processors.product_bestsellers",
                "main.context_processors.site_settings",
                "seo.context_processors.seo_metadata",
                "cart.context_processors.cart",
                "account.context_processors.auth_forms",
                "wishlist.context_processors.user_has_favorite",
            ],
        },
    },
]

WSGI_APPLICATION: str = "settings.wsgi.application"


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "uk-uk"

TIME_ZONE: str = "UTC"

USE_I18N: bool = True

USE_TZ: bool = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL: str = "static/"

MEDIA_URL: str = "media/"
MEDIA_ROOT: Path = BASE_DIR / MEDIA_URL

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

if DEBUG:
    STATICFILES_DIRS: list[Path] = [BASE_DIR / STATIC_URL]
else:
    STATIC_ROOT: Path = BASE_DIR / STATIC_URL

# Paginate settings
ITEMS_PER_PAGE: int = 4
ORDERS_PER_PAGE: int = 2

# Account
AUTH_USER_MODEL = "account.User"

# Cart
CART_SESSION_ID: str = "cart"

# Email
EMAIL_HOST: str | None = os.environ.get("EMAIL_HOST")
EMAIL_PORT: str | None = os.environ.get("EMAIL_PORT")
DEFAULT_FROM_EMAIL: str | None = os.environ.get("DEFAULT_FROM_EMAIL")

# DJANGO-META OG TAGS
META_SITE_PROTOCOL = os.environ.get("META_SITE_PROTOCOL")
META_SITE_DOMAIN = os.environ.get("META_SITE_DOMAIN")
META_SITE_NAME = os.environ.get("META_SITE_NAME")
META_SITE_TYPE = os.environ.get("META_SITE_TYPE")
META_USE_OG_PROPERTIES = True
META_DEFAULT_KEYWORDS = [
    item.strip() for item in os.environ.get("META_DEFAULT_KEYWORDS").split(",")
]

# CK EDITOR 5 START --------------------------------------------------------------------------------------------------
customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]
# CKEDITOR_5_CUSTOM_CSS = 'path_to.css' # optional
# CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage" # optional
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": {
            "items": [
                "heading",
                "|",
                "bold",
                "italic",
                "link",
                "bulletedList",
                "numberedList",
                "imageUpload",
            ],
        }
    },
    "extends": {
        "blockToolbar": [
            "paragraph",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
        ],
        "toolbar": {
            "items": [
                "heading",
                "|",
                "outdent",
                "indent",
                "|",
                "bold",
                "italic",
                "link",
                "alignment",
                "underline",
                "subscript",
                "superscript",
                "highlight",
                "|",
                "sourceEditing",
                "insertImage",
                "bulletedList",
                "numberedList",
                "fontSize",
                "fontColor",
                "fontBackgroundColor",
                "mediaEmbed",
                "removeFormat",
                "insertTable",
            ],
            "shouldNotGroupWhenFull": "true",
        },
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading",
                    "class": "ck-heading_heading2",
                },
            ]
        },
        "alignment": {
            "options": [
                "left",
                "center",
                "right",
                "justify",
            ]
        },
    },
    "list": {
        "properties": {
            "styles": "true",
            "startIndex": "true",
            "reversed": "true",
        }
    },
}

# Define a constant in settings.py to specify file upload permissions
CKEDITOR_5_FILE_UPLOAD_PERMISSION = (
    "staff"  # Possible values: "staff", "authenticated", "any"
)

# CK EDITOR 5 END --------------------------------------------------------------------------------------------
