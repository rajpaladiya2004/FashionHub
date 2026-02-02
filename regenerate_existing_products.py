import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from Hub.models import Product, ProductReview
from Hub.views import generate_auto_reviews

print("=" * 60)
print("AUTO-GENERATING REVIEWS FOR PRODUCTS WITH RATING")
print("=" * 60)

# Find products with rating/review_count but no reviews
products = Product.objects.filter(review_count__gt=0, rating__gt=0).exclude(reviews__is_auto_generated=True)

for product in products[:3]:  # First 3 products
    print(f"\n📦 Product: {product.name}")
    print(f"   Rating: {product.rating}")
    print(f"   Target Reviews: {product.review_count}")
    
    # Generate reviews
    generate_auto_reviews(product, product.review_count, product.rating, None)
    
    # Verify
    auto_count = product.reviews.filter(is_approved=True, is_auto_generated=True).count()
    print(f"   ✅ Generated {auto_count} auto reviews")
    
    # Show distribution
    print(f"   Distribution:")
    for rating in range(5, 0, -1):
        count = product.reviews.filter(is_approved=True, is_auto_generated=True, rating=rating).count()
        if count > 0:
            print(f"      {rating}⭐: {count}")

print("\n" + "=" * 60)
print("✅ Auto-generation complete for existing products")
print("=" * 60)
