#!/usr/bin/env python
"""
Test script to verify invoice generation
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from Hub.models import Order
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Get first order
try:
    order = Order.objects.first()
    if order:
        print(f"Testing with order: {order.order_number}")
        
        # Try to generate simple PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                                rightMargin=36, leftMargin=36,
                                topMargin=36, bottomMargin=30)
        
        elements = []
        styles = getSampleStyleSheet()
        
        elements.append(Paragraph(f"Invoice {order.order_number}", styles['Heading1']))
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(f"Order Date: {order.created_at}", styles['Normal']))
        
        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        print(f"✓ PDF generated successfully!")
        print(f"  PDF size: {len(pdf_bytes)} bytes")
        
        # Save to file for testing
        with open('test_invoice.pdf', 'wb') as f:
            f.write(pdf_bytes)
        print("✓ Saved as test_invoice.pdf")
        
    else:
        print("No orders found in database")
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
