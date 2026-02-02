import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from Hub.models import ProductReview

# Check all reviews
all_reviews = ProductReview.objects.all()
print(f"Total reviews: {all_reviews.count()}\n")

for review in all_reviews:
    print(f"ID: {review.id}")
    print(f"User: {review.user.username if review.user else 'N/A'}")
    print(f"Product: {review.product.name}")
    print(f"Rating: {review.rating}")
    print(f"Comment length: {len(review.comment)}")
    print(f"Comment: '{review.comment[:50] if review.comment else 'EMPTY'}'")
    print(f"is_auto_generated: {review.is_auto_generated}")
    print(f"is_approved: {review.is_approved}")
    print("---")
