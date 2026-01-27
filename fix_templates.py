import re
import os

def fix_templates():
    """Fix all template image references to use safe placeholders"""
    
    templates = [
        'Hub/templates/index.html',
        'Hub/templates/product-details.html',
        'Hub/templates/cart.html',
        'Hub/templates/wishlist.html',
        'Hub/templates/shop.html',
        'Hub/templates/header.html',
    ]
    
    for template_file in templates:
        if not os.path.exists(template_file):
            print(f"⚠️  {template_file} not found")
            continue
            
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix slider background-image: url('{{ slider.image.url }}')
        if 'slider.image.url' in content:
            # This is tricky since it's in style attribute, we need to wrap the style
            content = content.replace(
                "style=\"\n        background-image: url('{{ slider.image.url }}');",
                """style="
        {% if slider.image %}background-image: url('{{ slider.image.url }}');{% else %}background-color: #f0f0f0;{% endif %}"""
            )
            print(f"✓ Fixed slider.image in {template_file}")
        
        # Fix banner.image.url
        if 'banner.image.url' in content:
            content = content.replace(
                '<img src="{{ banner.image.url }}" alt="{{ banner.title }}">',
                '''{% if banner.image %}<img src="{{ banner.image.url }}" alt="{{ banner.title }}">{% else %}<img src="{% static 'assets/img/product/placeholder.jpg' %}" alt="{{ banner.title }}" style="background-color: #f0f0f0;">{% endif %}'''
            )
            print(f"✓ Fixed banner.image in {template_file}")
        
        # Fix product.image.url - make sure {% if product.image %} wraps all instances
        if 'product.image.url' in content and 'if product.image' not in content:
            # Replace unprotected product image calls
            content = content.replace(
                '<img src="{{ product.image.url }}" alt="{{ product.name }}">',
                '''{% if product.image %}<img src="{{ product.image.url }}" alt="{{ product.name }}">{% else %}<img src="{% static 'assets/img/product/placeholder.jpg' %}" alt="{{ product.name }}" style="background-color: #f0f0f0;">{% endif %}'''
            )
            print(f"✓ Fixed product.image in {template_file}")
        
        # Fix item.product.image.url for cart/wishlist
        if 'item.product.image.url' in content and 'if item.product.image' not in content:
            content = content.replace(
                '<img src="{{ item.product.image.url }}" alt="{{ item.product.name }}"',
                '''{% if item.product.image %}<img src="{{ item.product.image.url }}" alt="{{ item.product.name }}"{% else %}<img src="{% static 'assets/img/product/placeholder.jpg' %}" alt="{{ item.product.name }}" style="background-color: #f0f0f0;"'''
            )
            print(f"✓ Fixed item.product.image in {template_file}")
        
        # Write back if changed
        if content != original_content:
            with open(template_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  → Saved {template_file}")
        else:
            print(f"  → No changes needed for {template_file}")

if __name__ == '__main__':
    fix_templates()
    print("\n✓ All templates checked and fixed!")
