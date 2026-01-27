# Add Product Form - Field Reference Guide

## 📋 Complete Field List

### Section 1: Basic Information
```
✓ Product Name *          [Text Input] - Required
✓ SKU                     [Text Input] - e.g., USB-HUB-7PORT
✓ Category                [Dropdown] - TOP_DEALS, TOP_SELLING, TOP_FEATURED, RECOMMENDED
✓ Brand                   [Text Input] - e.g., Samsung, Apple
✓ Tags                    [Text Input] - Comma-separated: Quality, New, Trending
✓ Active                  [Checkbox] - Product is visible on site
✓ Top Deal                [Checkbox] - Featured in deals section
```

### Section 2: Pricing & Inventory
```
✓ Price *                 [Number Input] - Required, decimal (e.g., 29.99)
✓ Old Price               [Number Input] - For discount calculation (e.g., 39.99)
✓ Stock Quantity *        [Number Input] - Required, integer (e.g., 50)
✓ Rating                  [Number Input] - 0-5 scale with decimals (e.g., 4.5)
✓ Review Count            [Number Input] - Integer (e.g., 120)
```

### Section 3: Product Images
```
✓ Main Product Image *    [File Upload] - Required, single file, recommended 400x400px
✓ Gallery Images          [File Upload] - Optional, multiple files (Ctrl/Cmd to select)
```

### Section 4: Product Description
```
✓ Description             [Textarea] - 5 rows, full product details with features/benefits
```

### Section 5: Product Specifications (4-column grid)
```
✓ Weight                  [Text Input] - e.g., "2 lbs", "1.5 kg"
✓ Dimensions              [Text Input] - e.g., "12 × 16 × 19 in"
✓ Available Colors        [Text Input] - e.g., "Gray, Black, White"
✓ Available Sizes         [Text Input] - e.g., "S, M, L, XL"
```

### Section 6: Shipping & Care (2-column grid)
```
✓ Shipping Information    [Text Input] - e.g., "Standard shipping: $5.95"
✓ Care Instructions       [Text Input] - e.g., "Machine wash up to 40ºC/86ºF"
```

---

## 🎨 UI Organization

```
┌─────────────────────────────────────────────────────────────┐
│  Product Information                                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📋 Basic Information    │  💰 Pricing & Inventory          │
│  ├─ Product Name *       │  ├─ Price *        Old Price     │
│  ├─ SKU                  │  ├─ Stock Quantity *             │
│  ├─ Category             │  └─ Rating         Review Count  │
│  ├─ Brand                │                                   │
│  ├─ Tags                 │                                   │
│  └─ [✓] Active  Top Deal │                                   │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  🖼️ Product Images                                          │
│  ├─ Main Product Image * [Browse...] 400x400px recommended  │
│  └─ Additional Gallery Images [Browse...] Multiple allowed  │
│     Hold Ctrl/Cmd to select multiple images                 │
├─────────────────────────────────────────────────────────────┤
│  📝 Product Description                                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Enter detailed product description...                 │  │
│  │                                                         │  │
│  │                                                         │  │
│  └───────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  📏 Product Specifications                                   │
│  ├─ Weight      │ Dimensions │ Colors      │ Sizes          │
│  │  2 lbs       │ 12×16×19 in│ Gray, Black │ S, M, L        │
├─────────────────────────────────────────────────────────────┤
│  🚚 Shipping & Care                                          │
│  ├─ Shipping Information    │ Care Instructions             │
│  │  Standard: $5.95          │ Machine wash 40ºC            │
├─────────────────────────────────────────────────────────────┤
│                    [Add Product Button]                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 💡 Example: Complete Product Entry

```
Product Name: USB Hub 7-Port Powered Data Hub
SKU: USB-HUB-7PORT
Category: TOP_DEALS
Brand: TechPro
Tags: Quality, New, Electronics, USB

Price: $29.99
Old Price: $39.99
Stock: 50
Rating: 4.5
Review Count: 120

Main Image: usb-hub-main.jpg
Gallery: [usb-hub-side.jpg, usb-hub-ports.jpg, usb-hub-package.jpg]

Description:
High-speed 7-port USB 3.0 hub with individual power switches. 
Features:
- SuperSpeed USB 3.0 (5Gbps transfer rate)
- 7 individually controlled ports with LED indicators
- Includes 12V/2A power adapter for charging devices
- Compatible with Windows, Mac, Linux
- Plug and play, no drivers needed

Weight: 1.2 lbs
Dimensions: 5 × 3 × 1 in
Colors: Black, White
Sizes: Standard

Shipping: Free shipping on orders over $50, Standard delivery 3-5 days
Care: Wipe clean with soft cloth, avoid liquids
```

---

## 🔄 What Happens When You Submit

1. **Form Validation**
   - Checks required fields (name, price, stock, main image)
   - Validates number formats

2. **Product Creation**
   - Saves product to database with all fields
   - Auto-generates slug from product name
   - Uploads main image to `media/products/`

3. **Gallery Processing**
   - Loops through selected gallery images
   - Creates ProductImage record for each
   - Sets auto-incrementing order (1, 2, 3...)
   - Uploads to `media/products/`

4. **Success Response**
   - Shows success message: "Product 'USB Hub 7-Port' added successfully with 3 gallery images!"
   - Redirects to add_product page (ready for next product)

5. **Product Display**
   - Product appears in shop page
   - Product details page shows all info + gallery
   - Admin can edit in Django admin panel

---

## ⚠️ Important Notes

### Required Fields (Must Fill):
- Product Name
- Price
- Stock Quantity
- Main Product Image

### Optional But Recommended:
- SKU (for inventory tracking)
- Brand (for filtering)
- Tags (for features display)
- Description (for SEO and customer info)
- Old Price (to show discounts)
- Gallery Images (better product presentation)

### Field Tips:
- **Tags**: Separate with commas, will display as feature bullets
- **Colors**: List all available options, separated by commas
- **Sizes**: Use standard formats (S, M, L, XL or 32, 34, 36)
- **Dimensions**: Use consistent units (inches or cm)
- **Weight**: Include unit (lbs, kg, oz)

---

## 🎯 Access Requirements

**Only FashionHub admin user can access this page!**

If logged in as different user:
- Error message: "Access denied. Only FashionHub user can add products."
- Redirects to homepage

To access:
1. Logout current user (if any)
2. Login with username: `FashionHub`
3. Navigate to: http://127.0.0.1:8000/add-product/

---

## 📸 Gallery Upload Guide

### Single File Upload (Main Image):
1. Click "Browse..." button
2. Select one image file
3. Click "Open"
4. File name appears next to button

### Multiple File Upload (Gallery):
1. Click "Browse..." button
2. **Hold Ctrl (Windows) or Cmd (Mac)**
3. Click each image you want to add
4. Click "Open"
5. Shows "X files selected"

### Supported Formats:
- JPG/JPEG
- PNG
- GIF
- WebP

### Recommended Sizes:
- Main Image: 400x400px (square)
- Gallery Images: 400x400px (consistent size)
- File Size: Under 5MB each (faster loading)

---

## 🛠️ Troubleshooting

### Problem: Form doesn't submit
- Check all required fields are filled
- Ensure main image is selected
- Check browser console for errors

### Problem: Gallery images not showing
- Verify files are image formats (jpg, png, gif)
- Check MEDIA_URL is configured
- Ensure ProductImage model is imported in views

### Problem: Access denied error
- Verify logged in as 'FashionHub' user
- Check user.username in Django admin

### Problem: Images not uploading
- Verify `enctype="multipart/form-data"` in form tag
- Check `MEDIA_ROOT` in settings.py
- Ensure media/ folder has write permissions

---

**Ready to add products!** 🚀
Navigate to: http://127.0.0.1:8000/add-product/
