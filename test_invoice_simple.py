#!/usr/bin/env python
"""Test the simplified invoice generation"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from Hub.models import Order, OrderItem
from decimal import Decimal
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

print("=" * 60)
print("INVOICE DOWNLOAD TEST")
print("=" * 60)

try:
    # Get first order
    order = Order.objects.first()
    if not order:
        print("✗ No orders found in database")
        sys.exit(1)
    
    print(f"\n✓ Found order: {order.order_number}")
    print(f"  - User: {order.user.username}")
    print(f"  - Total: ₹{order.total_amount}")
    print(f"  - Items: {order.items.count()}")
    
    # Get items
    order_items = OrderItem.objects.filter(order=order)
    print(f"  - Order items count: {order_items.count()}")
    
    # Create PDF buffer
    print("\n📄 Generating PDF...")
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                            rightMargin=36, leftMargin=36,
                            topMargin=36, bottomMargin=30)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Simple invoice format
    elements.append(Paragraph(f'<b>INVOICE - {order.order_number}</b>', styles['Heading1']))
    elements.append(Spacer(1, 12))
    
    # Order info
    order_info = f"""
    <b>Invoice Date:</b> {order.created_at.strftime('%d %B %Y')}<br/>
    <b>Order Status:</b> {order.get_order_status_display()}<br/>
    <b>Payment Method:</b> {order.payment_method.upper()}<br/>
    <b>Payment Status:</b> {'Paid' if order.payment_status == 'PAID' else 'Pending'}<br/>
    """
    elements.append(Paragraph(order_info, styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Billing address
    elements.append(Paragraph('<b>BILLED TO:</b>', styles['Heading2']))
    elements.append(Paragraph(order.shipping_address.replace('\n', '<br/>'), styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Items table
    items_data = [['Item Name', 'Quantity', 'Unit Price', 'Total']]
    for item in order_items:
        item_total = Decimal(str(item.product_price)) * Decimal(str(item.quantity))
        items_data.append([
            item.product_name,
            str(item.quantity),
            f"₹{float(item.product_price):.2f}",
            f"₹{float(item_total):.2f}",
        ])
    
    items_table = Table(items_data, colWidths=[3.5*72, 1*72, 1.5*72, 1.5*72])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 12))
    
    # Totals
    totals_info = f"""
    <b>Subtotal:</b> ₹{float(order.subtotal):.2f}<br/>
    <b>Tax:</b> ₹{float(order.tax):.2f}<br/>
    <b>Shipping:</b> ₹{float(order.shipping_cost):.2f}<br/>
    <b style="font-size: 14">TOTAL: ₹{float(order.total_amount):.2f}</b>
    """
    elements.append(Paragraph(totals_info, styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Footer
    elements.append(Paragraph('<b>Thank you for your purchase!</b>', styles['Normal']))
    
    # Build PDF
    print("  ⏳ Building PDF...")
    doc.build(elements)
    pdf_data = buffer.getvalue()
    buffer.close()
    
    print(f"✓ PDF generated successfully!")
    print(f"  - PDF size: {len(pdf_data)} bytes")
    
    # Save to test file
    test_file = 'test_invoice_simple.pdf'
    with open(test_file, 'wb') as f:
        f.write(pdf_data)
    print(f"✓ Saved as {test_file}")
    
    print("\n" + "=" * 60)
    print("✓ INVOICE GENERATION TEST PASSED")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
