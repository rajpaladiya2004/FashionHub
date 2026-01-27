with open('Hub/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix unprotected product.image.url (without {% if product.image %})
# This appears 3 times in Top Selling, Top Featured, and Recommended sections

old_pattern = '''                                <div class="product-image w-img">
                                    <a href="{% url 'product-details' product.id %}">
                                        <img src="{{ product.image.url }}" alt="{{ product.name }}">
                                    </a>
                                </div>'''

new_pattern = '''                                <div class="product-image w-img">
                                    <a href="{% url 'product-details' product.id %}">
                                        {% if product.image %}
                                            <img src="{{ product.image.url }}" alt="{{ product.name }}">
                                        {% else %}
                                            <img src="{% static 'assets/img/product/placeholder.jpg' %}" alt="{{ product.name }}" style="background-color: #f0f0f0; width: 100%; height: auto;">
                                        {% endif %}
                                    </a>
                                </div>'''

count = content.count(old_pattern)
content = content.replace(old_pattern, new_pattern)

print(f"✓ Fixed {count} unprotected product.image.url calls in index.html")

with open('Hub/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ index.html updated successfully")
