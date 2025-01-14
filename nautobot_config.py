import os

from nautobot.core.settings import *  # noqa F401,F403
from nautobot.core.settings_funcs import is_truthy, parse_redis_connection

SECRET_KEY = "0"

DATABASES = {
    'default': {
        'NAME': 'nautobot',                         # Database name
        'USER': 'nautobot',                         # Database username
        'PASSWORD': os.getenv("NAUTOBOT_DB_PASSWORD", "nautobot"),                     # Database password
        'HOST': 'localhost',                        # Database server
        'PORT': '5432',                             # Database port (leave blank for default)
        'CONN_MAX_AGE': 300,                        # Max database connection age
        'ENGINE': 'django.db.backends.postgresql',  # Database driver ("mysql" or "postgresql")
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        "TIMEOUT": 300,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


JOBS_ROOT = "/home/adil/github/dev/nautobot/test_mock"
