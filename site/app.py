#!/usr/bin/env python

from coltrane import initialize
from django.core.management import execute_from_command_line

wsgi = initialize()

if __name__ == "__main__":
    execute_from_command_line()
