"""Configuracion local con una base SQLite independiente."""

from .settings import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db_local.sqlite3",  # noqa: F405
    }
}
