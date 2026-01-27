with open('Hub/templates/header.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add admin link in submenu after "My Account"
old_text = '''                                        <ul class="submenu">
                                            <li><a href="{% url 'profile' %}">My Account</a></li>
                                            <li><a href="{% url 'product-details' %}">Product Details</a></li>'''

new_text = '''                                        <ul class="submenu">
                                            <li><a href="{% url 'profile' %}">My Account</a></li>
                                            {% if user.username == 'admin' %}
                                            <li><a href="{% url 'add_product' %}" style="color: #fcbe00; font-weight: 600;">➕ Add Product</a></li>
                                            {% endif %}
                                            <li><a href="{% url 'product-details' %}">Product Details</a></li>'''

content = content.replace(old_text, new_text)

with open('Hub/templates/header.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Added 'Add Product' link in header (admin only)")
