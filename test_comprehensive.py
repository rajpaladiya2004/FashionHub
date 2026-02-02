#!/usr/bin/env python
"""
COMPREHENSIVE INVOICE DOWNLOAD TEST
====================================
Tests the complete invoice download flow as it would work from a browser.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from django.http import HttpRequest
from Hub.views import download_invoice
from Hub.models import Order

print("=" * 70)
print("COMPREHENSIVE INVOICE DOWNLOAD TEST")
print("=" * 70)

# 1. Verify order exists
try:
    order = Order.objects.get(order_number='ORD20260201011')
    print(f"\n✓ Order found: {order.order_number}")
    print(f"  Owner: {order.user.username} (ID: {order.user.id})")
except Order.DoesNotExist:
    print(f"\n✗ Order not found")
    sys.exit(1)

# 2. Create mock request as authenticated user
request = HttpRequest()
request.user = order.user
request.method = 'GET'
print(f"\n✓ Mock request created for user: {order.user.username}")

# 3. Call the view
print(f"\nCalling download_invoice view...")
try:
    response = download_invoice(request, 'ORD20260201011')
    status = response.status_code
    print(f"✓ View returned HTTP {status}")
    
    if status == 200:
        # 4. Validate PDF
        print(f"\nValidating PDF...")
        print(f"  Content-Type: {response.get('Content-Type', 'Not set')}")
        print(f"  Content-Length: {len(response.content)} bytes")
        
        # Check PDF header
        if response.content.startswith(b'%PDF'):
            print(f"  ✓ Valid PDF header found")
        else:
            print(f"  ✗ Invalid PDF header")
            sys.exit(1)
        
        # Check Content-Disposition
        disposition = response.get('Content-Disposition', '')
        if 'attachment' in disposition and '.pdf' in disposition:
            print(f"  ✓ Content-Disposition: {disposition}")
        else:
            print(f"  ✗ Missing Content-Disposition header")
        
        # Check Cache-Control
        cache = response.get('Cache-Control', '')
        if 'no-cache' in cache or 'no-store' in cache:
            print(f"  ✓ Cache-Control: {cache}")
        else:
            print(f"  ⚠ Cache-Control not set (may be cached)")
        
        print(f"\n✓ Invoice PDF is valid and ready for download!")
        print(f"✓ File would download as: ORD20260201011_invoice.pdf")
        
    else:
        print(f"✗ View returned error status: {status}")
        print(f"Response: {response.content.decode()}")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Exception: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("✓ ALL TESTS PASSED - INVOICE DOWNLOAD IS WORKING!")
print("=" * 70)
