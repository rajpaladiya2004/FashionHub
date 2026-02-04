import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashionHub.FashioHub.settings')

import sys
sys.path.insert(0, 'D:\\web\\FashioHub')
sys.path.insert(0, 'D:\\web\\FashioHub\\FashionHub')

django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("VibeMall Email Test - Simple Version")
print("=" * 60)
print(f"Backend: {settings.EMAIL_BACKEND}")
print(f"Host: {settings.EMAIL_HOST}")
print(f"User: {settings.EMAIL_HOST_USER}")
print(f"From: {settings.DEFAULT_FROM_EMAIL}")
print("=" * 60)

try:
    result = send_mail(
        subject='VibeMall Test Email',
        message='This is a test from VibeMall. Email configuration working!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['info.vibemall@gmail.com'],
        fail_silently=False,
    )
    print(f"\n[SUCCESS] Email sent! Result: {result}")
except Exception as e:
    print(f"\n[FAILED] Email error: {e}")
