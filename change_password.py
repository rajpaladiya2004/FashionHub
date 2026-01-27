import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from django.contrib.auth.models import User

try:
    user = User.objects.get(username='FashionHub')
    user.set_password('Paladiya@2023')
    user.save()
    print("✓ Password changed successfully!")
    print("  Username: FashionHub")
    print("  New Password: Paladiya@2023")
except User.DoesNotExist:
    print("❌ User 'FashionHub' not found")
