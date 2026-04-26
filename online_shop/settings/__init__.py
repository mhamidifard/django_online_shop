"""Select Django settings module based on DJANGO_ENV."""

import os

DJANGO_ENV = os.getenv("DJANGO_ENV", "development").strip().lower()

if DJANGO_ENV == "production":
    from .production import *  # noqa: F403
else:
    from .development import *  # noqa: F403
