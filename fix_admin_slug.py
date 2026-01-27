with open('Hub/admin.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove 'slug' from readonly_fields since it's in prepopulated_fields
content = content.replace(
    "readonly_fields = ('slug', 'image_preview')",
    "readonly_fields = ('image_preview',)"
)

with open('Hub/admin.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed: Removed slug from readonly_fields")
print("  Slug will now auto-populate from product name")
