#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
import django
django.setup()

from Hub.models import Order

order = Order.objects.get(order_number='ORD20260201011')
print(f"Order owner: {order.user.username}")
print(f"User ID: {order.user.id}")
