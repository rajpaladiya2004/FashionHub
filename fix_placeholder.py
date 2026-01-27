#!/usr/bin/env python
"""
Replace placeholder.jpg with tp-1.jpg in all templates
"""

import os

template_files = [
    'Hub/templates/index.html',
    'Hub/templates/product-details.html',
]

old_text = "{% static 'assets/img/product/placeholder.jpg' %}"
new_text = "{% static 'assets/img/product/tp-1.jpg' %}"

for file_path in template_files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        count = content.count(old_text)
        if count > 0:
            content = content.replace(old_text, new_text)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ Updated {file_path} ({count} replacements)")
        else:
            print(f"⚠ No placeholder found in {file_path}")
    else:
        print(f"✗ File not found: {file_path}")

print("\n✓ All templates updated!")
