#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

# Check the generated PDF file
pdf_path = 'invoice_test.pdf'
if os.path.exists(pdf_path):
    with open(pdf_path, 'rb') as f:
        content = f.read()
    
    # Decode to see text content
    text_content = content.decode('latin-1', errors='ignore')
    
    # Check for key elements
    checks = {
        'PDF header': content.startswith(b'%PDF'),
        'FashionHub': b'FashionHub' in content,
        'INVOICE': b'INVOICE' in content,
        'Rs': b'Rs' in content,
        'ORD20260201011': b'ORD20260201011' in content or 'ORD20260201011' in text_content,
    }
    
    print(f"Invoice PDF: {pdf_path} ({len(content)} bytes)")
    print("\nContent checks:")
    for key, result in checks.items():
        status = "✓" if result else "✗"
        print(f"  {status} {key}")
    
    # Try to extract some text
    print("\nSample of PDF text content:")
    for line in text_content.split('\n')[:20]:
        if line.strip() and len(line) > 5 and any(c.isprintable() for c in line):
            print(f"  {line.strip()[:80]}")
else:
    print(f"PDF not found at {pdf_path}")
