#!/usr/bin/env python
"""
Update all product action buttons in index.html
"""
import re

with open('Hub/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find and replace the eye icon button
content = re.sub(
    r'<a href="#" class="icon-box icon-box-1">\s*<i class="fal fa-eye"></i>\s*</a>',
    '<a href="javascript:void(0);" onclick="quickView({{ product.id }})" class="icon-box icon-box-1" title="Quick View">\n                                        <i class="fal fa-eye"></i>\n                                    </a>',
    content
)

# Pattern to find and replace the heart icon button
content = re.sub(
    r'<a href="#" class="icon-box icon-box-1">\s*<i class="fal fa-heart"></i>\s*</a>',
    '<a href="javascript:void(0);" onclick="addToWishlist({{ product.id }})" class="icon-box icon-box-1" title="Add to Wishlist">\n                                        <i class="fal fa-heart"></i>\n                                    </a>',
    content
)

# Pattern to find and replace the layer-group icon button
content = re.sub(
    r'<a href="#" class="icon-box icon-box-1">\s*<i class="fal fa-layer-group"></i>\s*</a>',
    '<a href="{% url \'product-details\' product.id %}" class="icon-box icon-box-1" title="View Details">\n                                        <i class="fal fa-layer-group"></i>\n                                    </a>',
    content
)

with open('Hub/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Updated all product action buttons!")
print("  - Quick View (eye icon) - triggers modal")
print("  - Add to Wishlist (heart icon) - adds to wishlist")
print("  - View Details (layer-group icon) - goes to product page")
