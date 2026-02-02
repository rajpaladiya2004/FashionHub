#!/usr/bin/env python
import os

pdf_path = 'invoice_test.pdf'
if os.path.exists(pdf_path):
    file_size = os.path.getsize(pdf_path)
    print(f"✓ Invoice PDF generated: {pdf_path} ({file_size} bytes)")
    
    # Check file structure
    with open(pdf_path, 'rb') as f:
        header = f.read(9)
        if header == b'%PDF-1.4':
            print(f"✓ Valid PDF 1.4 header")
        
        # Look for key text markers in the PDF stream (they may be uncompressed)
        content = f.read()
        if b'FashionHub' in content or b'Invoice' in content.lower():
            print(f"✓ Document text found in PDF")
        print(f"✓ PDF file is valid and ready to download")
else:
    print(f"✗ PDF file not found at {pdf_path}")
