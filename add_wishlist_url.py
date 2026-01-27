#!/usr/bin/env python
"""
Add AJAX wishlist URL to Hub/urls.py
"""

with open('Hub/urls.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the wishlist section and add the new URL
new_url = "    path('wishlist/add/<int:product_id>/', views.ajax_add_to_wishlist, name='ajax_add_to_wishlist'),\n"

# Insert after the existing wishlist URLs
for i, line in enumerate(lines):
    if 'add-to-wishlist' in line and 'name=' in line:
        # Insert the new URL after this line
        lines.insert(i + 1, new_url)
        break

with open('Hub/urls.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✓ Added AJAX wishlist URL route")
print("  URL: /wishlist/add/<product_id>/")
