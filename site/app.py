#!/usr/bin/env python

from coltrane import initialize
from django.core.management import execute_from_command_line

from os import getenv

env = {
    "GITHUB_USERNAME": getenv("GITHUB_USERNAME"),
    "GITHUB_PERSONAL_ACCESS_TOKEN": getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
}

wsgi = initialize(ENV=env)

if __name__ == "__main__":
    execute_from_command_line()
