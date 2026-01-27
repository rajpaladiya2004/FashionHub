#!/usr/bin/env python
"""
Script to assign product images to all products
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from Hub.models import Product

# Map category products to images
image_mapping = {
    # TOP DEALS
    'Solo3 Wireless Headphones': 'products/tp-1.jpg',
    'Beats Studio Pro': 'products/tp-2.jpg',
    'AirPods Max': 'products/tp-3.jpg',
    'JBL Flip 6': 'products/tp-4.jpg',
    
    # TOP SELLING
    'iPhone 15 Case': 'products/tp-5.jpg',
    'USB-C Cable': 'products/tp-6.jpg',
    'Wireless Charger': 'products/tp-7.jpg',
    'Phone Stand': 'products/tp-9.jpg',
    
    # TOP FEATURED
    'Premium Laptop Backpack': 'products/tp-10.jpg',
    'Mechanical Keyboard': 'products/tp-12.jpg',
    'Wireless Mouse': 'products/tp-13.jpg',
    'Monitor Stand': 'products/tp-14.jpg',
    
    # RECOMMENDED
    'Desk Lamp LED': 'products/tp-15.jpg',
    'Cable Organizer': 'products/tp-16.jpg',
    'USB Hub 7-Port': 'products/tp-17.jpg',
    'Webcam HD': 'products/tp-18.jpg',
}

products = Product.objects.all()
count = 0

for product in products:
    if product.name in image_mapping:
        product.image = image_mapping[product.name]
        product.save()
        print(f"✓ Assigned image to: {product.name} → {product.image}")
        count += 1
    else:
        print(f"⚠ No image mapping for: {product.name}")

print(f"\n✓ Total products updated: {count}/{products.count()}")
