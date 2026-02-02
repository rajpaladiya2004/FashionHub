#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from Hub.models import Order, OrderItem
from django.conf import settings

order = Order.objects.get(order_number='ORD20260201011')
items = OrderItem.objects.filter(order=order)

for item in items:
    print(f"Item: {item.product_name}")
    print(f"  product_image: {item.product_image}")
    print(f"  image repr: {repr(item.product_image)}")
    
    # Check if file exists
    media_root = getattr(settings, 'MEDIA_ROOT', None) or os.path.join(settings.BASE_DIR, 'media')
    img_path_str = str(item.product_image).strip()
    if img_path_str.startswith('/media/'):
        img_path_str = img_path_str[len('/media/'):]
    elif img_path_str.startswith('media/'):
        img_path_str = img_path_str[len('media/'):]
    elif img_path_str.startswith('/'):
        img_path_str = img_path_str[1:]
    img_path = os.path.join(media_root, img_path_str)
    print(f"  MEDIA_ROOT: {media_root}")
    print(f"  resolved path: {img_path}")
    print(f"  exists: {os.path.exists(img_path)}")
    if os.path.exists(img_path):
        print(f"  size: {os.path.getsize(img_path)} bytes")
