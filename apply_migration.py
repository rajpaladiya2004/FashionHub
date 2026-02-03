#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from django.core.management import call_command

try:
    call_command('migrate', 'Hub')
    print("Migration applied successfully!")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
