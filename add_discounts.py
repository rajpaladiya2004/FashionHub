#!/usr/bin/env python
"""
Script to add discount_percent to products
Add discount automatically based on old_price vs price difference
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from Hub.models import Product
from django.db import models
from decimal import Decimal

# Get all products that have an old_price but no discount_percent
products = Product.objects.filter(old_price__isnull=False).filter(
    models.Q(discount_percent=0) | models.Q(discount_percent__isnull=True)
)

updated_count = 0

for product in products:
    if product.old_price and product.old_price > product.price:
        # Calculate discount percentage
        discount = ((product.old_price - product.price) / product.old_price) * 100
        product.discount_percent = int(discount)
        product.save()
        updated_count += 1
        print(f"✓ {product.name}: {product.discount_percent}% discount added")

# Also add some discount to products without old_price (just for demo)
products_no_old_price = Product.objects.filter(old_price__isnull=True, discount_percent=0)[:5]
for product in products_no_old_price:
    product.discount_percent = 15  # 15% discount
    product.save()
    updated_count += 1
    print(f"✓ {product.name}: 15% discount added")

print(f"\n✓ Updated {updated_count} products with discount percentages!")
