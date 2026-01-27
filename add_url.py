with open('FashioHub/urls.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add the route before the closing ]
insert_pos = content.rfind(']')
new_route = "    path('add-product/', views.add_product, name='add_product'),\n"

content = content[:insert_pos] + new_route + content[insert_pos:]

with open('FashioHub/urls.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Added add-product URL route")
