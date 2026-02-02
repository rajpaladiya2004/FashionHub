#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User

client = Client()
user = User.objects.filter(is_staff=False).first()
if user:
    print(f"Testing with user: {user.username}")
    client.force_login(user)
    response = client.get('/order/download-invoice/ORD20260201011/')
    print(f'Status: {response.status_code}')
    print(f'Content-Type: {response.get("Content-Type")}')
    print(f'Content-Length: {response.get("Content-Length")}')
    if response.status_code == 200:
        print('✓ Invoice downloaded successfully!')
        # Save the PDF for inspection
        with open('test_invoice_download.pdf', 'wb') as f:
            f.write(response.content)
        print(f'✓ Saved to test_invoice_download.pdf ({len(response.content)} bytes)')
    else:
        print('✗ Error status:', response.status_code)
        print('Response:', response.content[:300])
else:
    print('✗ No non-staff users found')
