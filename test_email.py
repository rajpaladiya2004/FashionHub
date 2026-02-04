#!/usr/bin/env python
"""Test email configuration for VibeMall"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("📧 Testing VibeMall Email Configuration...")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print()

try:
    result = send_mail(
        subject='VibeMall Email Configuration Test ✅',
        message="""
Hello! 

This is a test email from VibeMall to verify your email configuration is working correctly.

If you received this email, it means:
✅ SMTP connection is successful
✅ Gmail App Password is correct
✅ Email sending is enabled for orders

Your FashioHub customers will now receive:
- Order confirmation emails
- Order status updates
- Customer support notifications

Best regards,
VibeMall Team
        """,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['rajpaladiya2023@gmail.com'],
        fail_silently=False
    )
    print(f"✅ Email sent successfully!")
    print(f"Status: {result} email(s) sent")
except Exception as e:
    print(f"❌ Error sending email:")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
