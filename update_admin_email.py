"""
Update admin email addresses to new VibeMall email
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
from Hub.models import AdminEmailSettings

print("=" * 60)
print("Updating Admin Email Addresses")
print("=" * 60)

# Update all superuser emails
superusers = User.objects.filter(is_superuser=True)
print(f"\nFound {superusers.count()} superuser(s)")

for user in superusers:
    old_email = user.email
    user.email = 'info.vibemall@gmail.com'
    user.save()
    print(f"✓ Updated {user.username}: {old_email} → info.vibemall@gmail.com")

# Update or create AdminEmailSettings
admin_settings, created = AdminEmailSettings.objects.get_or_create(
    setting_name='order_notifications',
    defaults={
        'admin_email': 'info.vibemall@gmail.com',
        'is_active': True
    }
)

if not created:
    admin_settings.admin_email = 'info.vibemall@gmail.com'
    admin_settings.is_active = True
    admin_settings.save()
    print(f"\n✓ Updated AdminEmailSettings: {admin_settings.admin_email}")
else:
    print(f"\n✓ Created AdminEmailSettings: {admin_settings.admin_email}")

print("\n" + "=" * 60)
print("Admin email update complete!")
print("All admin notifications will now go to: info.vibemall@gmail.com")
print("=" * 60)
