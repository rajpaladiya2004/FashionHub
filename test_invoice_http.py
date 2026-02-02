#!/usr/bin/env python
"""
Simulate the exact HTTP request to download invoice.
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
import django
django.setup()

import requests
from django.contrib.auth.models import User

# Get a non-staff user to login
user = User.objects.filter(is_staff=False).first()
if not user:
    print("✗ No non-staff users found")
    exit(1)

print(f"Testing with user: {user.username}")
print(f"Order: ORD20260201011")
print()

# Try to access the invoice download URL directly via requests
# This will fail since we need session/auth, but let's try via django test client workaround
from django.test import Client

client = Client()
# Login the user
logged_in = client.login(username=user.username, password='test123')  # This will fail but let's see
print(f"Login attempt: {logged_in}")

# Try accessing the invoice endpoint
print("Attempting to download invoice...")
try:
    # Make a raw request to test the download_invoice view directly
    from Hub.views import download_invoice
    from django.http import HttpRequest
    from django.contrib.sessions.middleware import SessionMiddleware
    
    # Create fake request
    request = HttpRequest()
    request.user = user
    request.method = 'GET'
    request.path = '/order/download-invoice/ORD20260201011/'
    
    # Call the view directly
    response = download_invoice(request, 'ORD20260201011')
    
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.get('Content-Type')}")
    print(f"Content-Length: {response.get('Content-Length')}")
    
    if response.status_code == 200:
        print("✓ Invoice downloaded successfully!")
        # Save the PDF
        with open('test_http_download.pdf', 'wb') as f:
            f.write(response.content)
        print(f"✓ Saved to test_http_download.pdf ({len(response.content)} bytes)")
    else:
        print(f"✗ Error status: {response.status_code}")
        if hasattr(response, 'content'):
            print(f"Response: {response.content[:500]}")
        
except Exception as e:
    print(f"✗ Exception: {e}")
    import traceback
    traceback.print_exc()
