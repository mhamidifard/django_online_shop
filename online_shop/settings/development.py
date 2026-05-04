"""Development settings."""

from .base import *  # noqa: F403,F401

DEBUG = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Import Celery configuration for development
from .celery_development import *  # noqa: F403,F401
