with open('Hub/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove duplicate if banner.image
old = '''{% if banner.image %}{% if banner.image %}<img src="{{ banner.image.url }}" alt="{{ banner.title }}">{% else %}<img src="{% static 'assets/img/product/placeholder.jpg' %}" alt="{{ banner.title }}" style="background-color: #f0f0f0;">{% endif %}{% else %}<img src="{% static 'assets/img/product/placeholder.jpg' %}" alt="{{ banner.title }}" style="background-color: #f0f0f0;">{% endif %}'''

new = '''{% if banner.image %}<img src="{{ banner.image.url }}" alt="{{ banner.title }}">{% else %}<img src="{% static 'assets/img/product/placeholder.jpg' %}" alt="{{ banner.title }}" style="background-color: #f0f0f0;">{% endif %}'''

if old in content:
    content = content.replace(old, new)
    print("✓ Removed duplicate banner.image checks")
else:
    print("⚠️ Duplicate banner.image not found (might already be cleaned)")

with open('Hub/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ index.html cleaned up")
