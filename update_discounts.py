#!/usr/bin/env python
"""
Direct Python script to update discount percentages
Run with: python update_discounts.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
sys.path.insert(0, 'd:\\web\\FashioHub')

django.setup()

from Hub.models import Product

print("Updating product discounts...\n")

# Update all products
all_products = Product.objects.all()
updated = 0

for product in all_products:
    # If product has old_price and it's higher than current price, calculate discount
    if product.old_price and product.old_price > product.price:
        discount = int(((product.old_price - product.price) / product.old_price) * 100)
        if discount > 0 and product.discount_percent == 0:
            product.discount_percent = discount
            product.save()
            print(f"✓ {product.name}: {discount}% discount")
            updated += 1
    
    # If no old_price but discount_percent is 0, add a default discount for demo
    elif not product.old_price and product.discount_percent == 0:
        product.discount_percent = 10
        product.save()
        print(f"✓ {product.name}: 10% discount (demo)")
        updated += 1

print(f"\n✓ Total products updated: {updated}")
