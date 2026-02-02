import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from Hub.models import Product
from django.db.models import Count

print("=" * 60)
print("TESTING AUTOMATIC CATEGORIZATION")
print("=" * 60)

# Test TOP_SELLING
top_selling = Product.objects.filter(
    is_active=True,
    sold__gt=0
).order_by('-sold')[:5]

print(f"\nTOP_SELLING (Top 5 by sold count):")
for p in top_selling:
    print(f"  - {p.name}: {p.sold} sold (currently: {p.category})")

# Test TOP_DEALS
top_deals = Product.objects.filter(
    is_active=True,
    discount_percent__gt=0
).order_by('-discount_percent')[:5]

print(f"\nTOP_DEALS (Top 5 by discount):")
for p in top_deals:
    print(f"  - {p.name}: {p.discount_percent}% off (currently: {p.category})")

# Test RECOMMENDED (by wishlist)
from Hub.models import Wishlist
from django.utils import timezone
from datetime import timedelta

thirty_days_ago = timezone.now() - timedelta(days=30)
recommended = Product.objects.filter(
    is_active=True,
    wishlist__created_at__gte=thirty_days_ago
).annotate(
    wishlist_count=Count('wishlist')
).order_by('-wishlist_count')[:5]

print(f"\nRECOMMENDED (Top 5 by wishlist):")
for p in recommended:
    print(f"  - {p.name}: {p.wishlist_count} wishlists (currently: {p.category})")

# Test TOP_FEATURED (by rating)
top_featured = Product.objects.filter(
    is_active=True,
    rating__gte=4.0,
    review_count__gte=1
).order_by('-rating', '-review_count')[:5]

print(f"\nTOP_FEATURED (Top 5 by rating):")
for p in top_featured:
    print(f"  - {p.name}: {p.rating}⭐ ({p.review_count} reviews, currently: {p.category})")

print("\n" + "=" * 60)
print("Ready to auto-categorize!")
print("=" * 60)
