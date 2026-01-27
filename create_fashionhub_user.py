import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from django.contrib.auth.models import User

# Check if FashionHub user exists
if User.objects.filter(username='FashionHub').exists():
    print("✓ User 'FashionHub' already exists")
else:
    # Create FashionHub superuser
    user = User.objects.create_superuser(
        username='FashionHub',
        email='fashionhub@admin.com',
        password='FashionHub@123'
    )
    print("✓ Created superuser 'FashionHub'")
    print("  Username: FashionHub")
    print("  Password: FashionHub@123")
    print("  Email: fashionhub@admin.com")
