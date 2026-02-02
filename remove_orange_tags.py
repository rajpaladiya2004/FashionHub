import re

# Read the file
filepath = r'd:\web\FashioHub\Hub\templates\index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match the orange discount tag section with more specific match
pattern = r'<!-- DISCOUNT TAG ABOVE NAME -->\s*{% if product\.old_price and product\.price < product\.old_price %}\s*<div style="margin-bottom: 6px;">\s*<span[^>]*>\s*-\{\{ product\.old_price\|calc_discount:product\.price \}\}% OFF\s*</span>\s*</div>\s*{% endif %}\s*'

# Replace pattern with empty string
content = re.sub(pattern, '', content)

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Orange discount tags removed!")

