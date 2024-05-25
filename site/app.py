#!/usr/bin/env python

from coltrane import initialize
from django.core.management import execute_from_command_line
from sys import argv


is_compress_offline = False

if len(argv) > 1 and argv[1] == "compress":
    is_compress_offline = True

wsgi = initialize(COMPRESS_OFFLINE=is_compress_offline)

if __name__ == "__main__":    
    execute_from_command_line()
