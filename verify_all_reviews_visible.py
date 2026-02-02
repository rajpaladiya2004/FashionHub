import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from Hub.models import Product

product = Product.objects.filter(review_count__gt=0).first()
if product:
    print(f'Product: {product.name}')
    print(f'Rating: {product.rating}')
    print()
    
    all_reviews = product.reviews.filter(is_approved=True)
    auto = all_reviews.filter(is_auto_generated=True).count()
    customer = all_reviews.filter(is_auto_generated=False).count()
    
    print(f'Total Reviews: {all_reviews.count()}')
    print(f'  Auto-generated: {auto} (now visible ✅)')
    print(f'  Customer: {customer}')
    print()
    print('Distribution:')
    for rating in range(5, 0, -1):
        count = all_reviews.filter(rating=rating).count()
        if count > 0:
            print(f'  {rating}⭐: {count}')
