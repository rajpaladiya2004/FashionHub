import re

# Read the file
with open(r'd:\web\FashioHub\Hub\templates\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match orange discount tags
patterns = [
    # Pattern 1: Complete discount tag block with comment
    r'\s*<!-- DISCOUNT TAG ABOVE NAME -->\s*{% if product\.old_price and product\.price < product\.old_price %}\s*<div style="margin-bottom: \d+px;">\s*<span style="[^"]*background: #ff6b35[^"]*">\s*-[^<]+</span>\s*</div>\s*{% endif %}\s*\n*',
    
    # Pattern 2: Without comment
    r'\s*{% if product\.old_price and product\.price < product\.old_price %}\s*<div style="margin-bottom: \d+px;">\s*<span style="[^"]*background: #ff6b35[^"]*">\s*-[^<]+</span>\s*</div>\s*{% endif %}\s*\n*',
]

# Remove all orange tags
for pattern in patterns:
    content = re.sub(pattern, '\n', content, flags=re.MULTILINE)

# Write back
with open(r'd:\web\FashioHub\Hub\templates\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ All orange discount tags removed successfully!")
