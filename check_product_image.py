#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from Hub.models import Product, OrderItem, Order

# Get the order
order = Order.objects.get(order_number='ORD20260201011')
order_items = OrderItem.objects.filter(order=order)

print("Order Items and their images:")
print("=" * 70)

for item in order_items:
    print(f"\nProduct: {item.product_name}")
    print(f"  product_image field: {item.product_image}")
    print(f"  product_image type: {type(item.product_image)}")
    
    if item.product_image:
        img_path = str(item.product_image).strip()
        print(f"  Image path (raw): {img_path}")
        
        # Normalize path
        if img_path.startswith('/media/'):
            img_path = img_path[len('/media/'):]
        elif img_path.startswith('media/'):
            img_path = img_path[len('media/'):]
        elif img_path.startswith('/'):
            img_path = img_path[1:]
        
        from django.conf import settings
        media_root = getattr(settings, 'MEDIA_ROOT', None) or os.path.join(settings.BASE_DIR, 'media')
        full_path = os.path.join(media_root, img_path)
        
        print(f"  Image path (normalized): {img_path}")
        print(f"  Full path: {full_path}")
        print(f"  Exists: {os.path.exists(full_path)}")
        
        if os.path.exists(full_path):
            print(f"  File size: {os.path.getsize(full_path)} bytes")
            print(f"  File extension: {os.path.splitext(full_path)[1].lower()}")
