import re

# File path
filepath = r'd:\web\FashioHub\FashionHub\Hub\templates\index.html'

# Read file
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match orange discount tags
pattern = r'\s*<!-- DISCOUNT TAG ABOVE NAME -->\s*{% if product\.old_price and product\.price < product\.old_price %}\s*<div style="[^"]*">\s*<span style="[^"]*#ff6b35[^"]*">\s*-[^<]+</span>\s*</div>\s*{% endif %}\s*'

# Remove all matches
content = re.sub(pattern, '\n', content, flags=re.MULTILINE)

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Orange tags removed from {filepath}")
