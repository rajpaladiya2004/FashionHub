import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from Hub.models import Product

product = Product.objects.filter(review_count__gt=0).first()
if product:
    print(f'Product: {product.name}')
    print(f'Rating: {product.rating}')
    print(f'Review Count Target: {product.review_count}')
    print()
    print('Auto-generated (hidden from customers):')
    auto = product.reviews.filter(is_auto_generated=True, is_approved=True)
    print(f'  Count: {auto.count()}')
    print()
    print('Customer reviews (displayed on product page):')
    customer = product.reviews.filter(is_auto_generated=False, is_approved=True)
    print(f'  Count: {customer.count()}')
    for rev in customer:
        comment = rev.comment[:30] if rev.comment else "(no comment)"
        print(f'    - {rev.name}: {rev.rating}⭐ - {comment}')
