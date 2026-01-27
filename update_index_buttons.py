#!/usr/bin/env python
"""
Update product action buttons in index.html to add quick view and wishlist functionality
"""

with open('Hub/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Old button structure
old_buttons = '''                                <!-- ACTION ICONS -->
                                <div class="product-action">
                                    <a href="#" class="icon-box icon-box-1">
                                        <i class="fal fa-eye"></i>
                                    </a>
                                    <a href="#" class="icon-box icon-box-1">
                                        <i class="fal fa-heart"></i>
                                    </a>
                                    <a href="#" class="icon-box icon-box-1">
                                        <i class="fal fa-layer-group"></i>
                                    </a>
                                </div>'''

# New button structure with onclick handlers
new_buttons = '''                                <!-- ACTION ICONS -->
                                <div class="product-action">
                                    <a href="javascript:void(0);" onclick="quickView({{ product.id }})" class="icon-box icon-box-1" title="Quick View">
                                        <i class="fal fa-eye"></i>
                                    </a>
                                    <a href="javascript:void(0);" onclick="addToWishlist({{ product.id }})" class="icon-box icon-box-1" title="Add to Wishlist">
                                        <i class="fal fa-heart"></i>
                                    </a>
                                    <a href="{% url 'product-details' product.id %}" class="icon-box icon-box-1" title="View Details">
                                        <i class="fal fa-layer-group"></i>
                                    </a>
                                </div>'''

# Replace all occurrences
count = content.count(old_buttons)
content = content.replace(old_buttons, new_buttons)

# Write back
with open('Hub/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✓ Updated {count} product action button sections")
print("✓ Quick view and wishlist buttons now functional!")
