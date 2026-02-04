"""
Test admin order notification email
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashionHub.FashioHub.settings')
sys.path.insert(0, 'D:\\web\\FashioHub')
sys.path.insert(0, 'D:\\web\\FashioHub\\FashionHub')
django.setup()

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

print("=" * 60)
print("Testing Admin Order Notification Email")
print("=" * 60)

# Get admin emails
admin_users = User.objects.filter(is_superuser=True)
admin_emails = [admin.email for admin in admin_users if admin.email]

print(f"\nAdmin Users Found: {admin_users.count()}")
for admin in admin_users:
    print(f"  - {admin.username}: {admin.email}")

print(f"\nAdmin Emails: {admin_emails}")
print(f"Email Backend: {settings.EMAIL_BACKEND}")
print(f"Email From: {settings.EMAIL_HOST_USER}")

# Send test email
try:
    subject = '🔔 Test Order Notification - VibeMall'
    text_content = """
New Order Received - Test

This is a test email to verify admin order notifications are working.

Customer: Test Customer
Email: test@example.com
Total Amount: ₹1000
Payment Method: COD

Best regards,
VibeMall System
    """
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=admin_emails
    )
    email.send(fail_silently=False)
    
    print(f"\n✅ SUCCESS! Test email sent to {len(admin_emails)} admin(s)")
    for admin_email in admin_emails:
        print(f"   ✓ {admin_email}")
        
except Exception as e:
    print(f"\n❌ FAILED! Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
