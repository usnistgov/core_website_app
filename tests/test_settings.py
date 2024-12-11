"""  Test settings
"""

from django.conf import settings

SECRET_KEY = "fake-key"
SERVER_URI = "http://localhost"

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.messages",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.sessions",
    # Extra apps
    "captcha",
    # Local app
    "tests",
    "core_main_app",
    "core_website_app",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["null"],
            "propagate": True,
            "level": "WARN",
        },
        "django.db.backends": {
            "handlers": ["null"],
            "level": "DEBUG",
            "propagate": False,
        },
        "": {  # use 'MYAPP' to make it app specific
            "handlers": ["null"],
            "level": "DEBUG",
        },
    },
}
WEBSITE_CONTACTS = [
    ("admin1", "admin1@example.com"),
    ("admin2", "admin2@example.com"),
]

MIDDLEWARE = (  # noqa
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core_main_app.utils.custom_context_processors.domain_context_processor",
                "django.template.context_processors.i18n",
            ],
        },
    },
]
# IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

SEND_EMAIL_WHEN_CONTACT_MESSAGE_IS_RECEIVED = getattr(
    settings, "SEND_EMAIL_WHEN_CONTACT_MESSAGE_IS_RECEIVED", True
)
""" boolean: send an email when a contact message is received
"""

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

SEND_EMAIL_WHEN_ACCOUNT_REQUEST_IS_ACCEPTED = getattr(
    settings, "SEND_EMAIL_WHEN_ACCOUNT_REQUEST_IS_ACCEPTED", False
)
SEND_EMAIL_WHEN_ACCOUNT_REQUEST_IS_DENIED = getattr(
    settings, "SEND_EMAIL_WHEN_ACCOUNT_REQUEST_IS_DENIED", False
)
ROOT_URLCONF = "tests.urls"

MONGODB_INDEXING = False
MONGODB_ASYNC_SAVE = False
