#!/usr/bin/env python

from os import getenv

from coltrane import initialize
from django.core.management import execute_from_command_line

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

redis_url = getenv("REDIS_URL")

if redis_url:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": redis_url,
        }
    }

wsgi = initialize(
    CACHES=CACHES,
    GITHUB_USERNAME=getenv("GITHUB_USERNAME"),
    GITHUB_PERSONAL_ACCESS_TOKEN=getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
)

if __name__ == "__main__":
    execute_from_command_line()
