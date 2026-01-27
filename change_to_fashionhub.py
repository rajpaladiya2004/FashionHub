import os

# Fix views.py - change 'admin' to 'FashionHub'
with open('Hub/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "if request.user.username != 'admin':",
    "if request.user.username != 'FashionHub':"
)
content = content.replace(
    "messages.error(request, 'Access denied. Only admin can add products.')",
    "messages.error(request, 'Access denied. Only FashionHub user can add products.')"
)

with open('Hub/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Updated views.py - changed access from 'admin' to 'FashionHub'")

# Fix header.html - change 'admin' to 'FashionHub'
with open('Hub/templates/header.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "{% if user.username == 'admin' %}",
    "{% if user.username == 'FashionHub' %}"
)

with open('Hub/templates/header.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Updated header.html - menu link now shows for 'FashionHub' user")
print("\n✅ Done! Now only user 'FashionHub' can access Add Product page")
