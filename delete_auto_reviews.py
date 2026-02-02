import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from Hub.models import ProductReview

# Delete all reviews with empty comment (auto-generated ones)
deleted = ProductReview.objects.filter(comment="").delete()
print(f"✅ Deleted {deleted[0]} auto-generated reviews")

# Verify
remaining = ProductReview.objects.all().count()
print(f"✅ Remaining customer reviews: {remaining}")
