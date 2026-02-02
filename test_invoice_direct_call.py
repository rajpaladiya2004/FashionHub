#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from django.http import HttpRequest
from django.contrib.auth.models import User
from Hub.views import download_invoice
from Hub.models import Order

# Get the order
order = Order.objects.get(order_number='ORD20260201011')
print(f"Order: {order.order_number}, User: {order.user.username}")

# Create a mock request with an authenticated user
request = HttpRequest()
request.user = order.user
request.method = 'GET'

# Call the view directly
try:
    print("\nCalling download_invoice view...")
    response = download_invoice(request, 'ORD20260201011')
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(f"✓ PDF generated successfully ({len(response.content)} bytes)")
        # Check if it's a valid PDF
        if response.content.startswith(b'%PDF'):
            print("✓ Valid PDF header found")
            # Save to file for inspection
            with open('invoice_test.pdf', 'wb') as f:
                f.write(response.content)
            print("✓ Saved to invoice_test.pdf")
        else:
            print(f"✗ Invalid PDF: starts with {response.content[:50]}")
    else:
        content = response.content.decode() if isinstance(response.content, bytes) else response.content
        print(f"✗ Error ({response.status_code}): {content}")
except Exception as e:
    print(f"✗ Exception: {e}")
    import traceback
    traceback.print_exc()
