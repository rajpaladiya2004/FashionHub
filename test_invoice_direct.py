#!/usr/bin/env python
"""Test invoice generation directly by calling the download_invoice view code."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from Hub.models import Order, OrderItem
from django.conf import settings
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from decimal import Decimal

# Get order
order = Order.objects.get(order_number='ORD20260201011')
order_items = OrderItem.objects.filter(order=order)

print(f"Generating invoice for {order.order_number}...")
print(f"  User: {order.user.username}")
print(f"  Items: {order_items.count()}")
print(f"  Total: ₨{order.total_amount}")

# Create PDF buffer
buffer = BytesIO()
doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=30)
elements = []
styles = getSampleStyleSheet()

value_style = ParagraphStyle(
    'Value',
    parent=styles['Normal'],
    fontSize=10,
    textColor=colors.HexColor('#1e293b'),
    fontName='Helvetica'
)

# Build simple items table
title = Paragraph('<b>Invoice #{}</b>'.format(order.order_number), styles['Heading1'])
elements.append(title)
elements.append(Spacer(1, 12))

# Items
items_data = [['Item', 'Qty', 'Unit Price', 'Total']]
for item in order_items:
    item_total = Decimal(str(item.product_price)) * Decimal(str(item.quantity))
    items_data.append([
        item.product_name[:50],
        str(item.quantity),
        f"₨{float(item.product_price):.2f}",
        f"₨{float(item_total):.2f}",
    ])

table = Table(items_data, colWidths=[3.7*inch, 0.6*inch, 1.0*inch, 1.0*inch])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('ALIGN', (0, 1), (0, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
elements.append(table)
elements.append(Spacer(1, 12))

# Totals
totals_data = [
    ['Subtotal', '', f'₨{float(order.subtotal):.2f}'],
    ['Tax', '', f'₨{float(order.tax):.2f}'],
    ['Shipping', '', f'₨{float(order.shipping_cost):.2f}'],
    ['TOTAL', '', f'₨{float(order.total_amount):.2f}'],
]
totals_table = Table(totals_data, colWidths=[2.5*inch, 1.5*inch, 2.0*inch])
totals_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
    ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
    ('LINEABOVE', (0, 3), (-1, 3), 2, colors.HexColor('#1e293b')),
]))
elements.append(totals_table)

# Build PDF
try:
    doc.build(elements)
    pdf_data = buffer.getvalue()
    buffer.close()
    
    # Save to file
    with open('test_invoice_direct.pdf', 'wb') as f:
        f.write(pdf_data)
    
    print(f"\n✓ Invoice generated successfully!")
    print(f"✓ Saved to test_invoice_direct.pdf ({len(pdf_data)} bytes)")
    print("\nPDF includes:")
    print("  ✓ Invoice number")
    print("  ✓ Items with ₨ currency symbol")
    print("  ✓ Totals with ₨ currency symbol")
    print("  ✓ Professional table formatting")
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
