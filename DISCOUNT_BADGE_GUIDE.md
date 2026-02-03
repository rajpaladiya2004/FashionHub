# Green Discount Badge Setup Guide

## Problem
The green discount badge is not showing on product cards because products don't have `discount_percent` values set.

## Solution
The green discount badge CSS is already in place:
- **Color**: Green (#5aab19)
- **Location**: Bottom-left corner of product image
- **Template Location**: `Hub/templates/shop.html` (line 23)

## How to Add Discount Percentages

### Option 1: Add Discount to Specific Products (Admin Panel)
1. Go to Django Admin (/admin/)
2. Navigate to Products
3. For each product, fill in the `discount_percent` field
4. Click Save

### Option 2: Bulk Update via Script
Run the script to automatically calculate and add discounts:

```bash
cd d:\web\FashioHub
python update_discounts.py
```

This will:
- Calculate discount from `old_price` vs `price` difference
- Add default 10% discount to products without old_price
- Display results in terminal

### Option 3: Manual Database Update
If you want to set discount directly in the template or database:

**For a product with old_price:**
- The badge will show if `discount_percent > 0`
- Example: If old_price=₹740, current_price=₹680
  - Discount = ((740-680)/740) × 100 = 8.1% → rounds to 8%

## Test the Badge
After adding discount_percent values:
1. Reload the shop page
2. You should see green badges on product cards with discounts
3. Badge shows: "-{discount_percent}%"

## Customization
To change badge color, edit in `shop.html` line 23:
```css
.discount-badge { 
    background: #5aab19;  /* Change this color */
    ...
}
```

Green color codes to try:
- Bright Green: #22C55E
- Forest Green: #16A34A
- Emerald: #10B981
- Current: #5aab19 (Olive Green)
