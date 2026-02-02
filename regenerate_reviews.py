import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from Hub.models import Product, ProductReview
from django.contrib.auth.models import User

# Get the first product with rating/review_count
products = Product.objects.filter(review_count__gt=0, rating__gt=0).order_by('-id')

for product in products[:1]:  # Just first one for testing
    print(f"\nProduct: {product.name}")
    print(f"Rating: {product.rating}")
    print(f"Review Count: {product.review_count}")
    print(f"Current approved reviews: {product.reviews.filter(is_approved=True).count()}")
    
    # Now re-generate
    missing = product.review_count - product.reviews.filter(is_approved=True).count()
    
    if missing > 0:
        print(f"Need to generate {missing} more reviews")
        
        # Call the generate_auto_reviews function from views
        from Hub.views import generate_auto_reviews
        generate_auto_reviews(product, product.review_count, product.rating, None)
        
        print(f"After regeneration: {product.reviews.filter(is_approved=True).count()} reviews")
        print("Reviews now have EMPTY comments (no text)")

print("\nDone!")
