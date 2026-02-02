#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

from Hub.models import Order

# Get the order owner
try:
    order = Order.objects.get(order_number='ORD20260201011')
    print(f"Order found: {order.order_number}")
    print(f"Order user: {order.user.username} (ID: {order.user.id})")
except Order.DoesNotExist:
    print("Order not found")
    sys.exit(1)

# Create a test client
client = Client()

# Login as the order owner
login_success = client.login(username='FashionHub', password='FashionHub123')
print(f"Login successful: {login_success}")

# Try to download the invoice
print("\nAttempting to download invoice...")
response = client.get(f'/order/download-invoice/ORD20260201011/')
print(f"Status Code: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type', 'Not set')}")
print(f"Content-Disposition: {response.get('Content-Disposition', 'Not set')}")

if response.status_code == 200:
    print(f"✓ PDF generated successfully ({len(response.content)} bytes)")
    # Check if it's a valid PDF
    if response.content.startswith(b'%PDF'):
        print("✓ Valid PDF header found")
    else:
        print(f"✗ Invalid PDF: starts with {response.content[:20]}")
elif response.status_code == 404:
    print(f"✗ 404 Error: {response.content.decode()}")
elif response.status_code == 500:
    print(f"✗ 500 Error: {response.content.decode()}")
else:
    print(f"✗ Unexpected status: {response.status_code}")
    print(f"Response: {response.content[:200]}")
