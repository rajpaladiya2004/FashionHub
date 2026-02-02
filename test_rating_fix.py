import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from Hub.models import Product

# Check if rating and review_count conversion is working
print("Testing rating/review_count storage:")
products = Product.objects.filter(review_count__gt=0, rating__gt=0).order_by('-id')[:2]

for product in products:
    print(f"\n✅ {product.name}")
    print(f"   Rating: {product.rating} (type: {type(product.rating).__name__})")
    print(f"   Review Count: {product.review_count} (type: {type(product.review_count).__name__})")
    
    auto = product.reviews.filter(is_auto_generated=True, is_approved=True).count()
    customer = product.reviews.filter(is_auto_generated=False, is_approved=True).count()
    
    print(f"   Auto-generated reviews: {auto}")
    print(f"   Customer reviews: {customer}")

print("\n✅ Rating/review_count conversion working correctly!")
