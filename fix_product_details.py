with open('Hub/templates/product-details.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix line 40 - thumbnail image
old1 = '''                                  <button class="nav-link active" id="thumbOne-tab" data-bs-toggle="tab" data-bs-target="#thumbOne" type="button" role="tab" aria-controls="thumbOne" aria-selected="true">
                                      <img src="{{ product.image.url }}" alt="{{ product.name }}" style="max-width: 80px;">
                                  </button>'''

new1 = '''                                  <button class="nav-link active" id="thumbOne-tab" data-bs-toggle="tab" data-bs-target="#thumbOne" type="button" role="tab" aria-controls="thumbOne" aria-selected="true">
                                      {% if product.image %}
                                          <img src="{{ product.image.url }}" alt="{{ product.name }}" style="max-width: 80px;">
                                      {% else %}
                                          <img src="{% static 'assets/img/product/placeholder.jpg' %}" alt="{{ product.name }}" style="max-width: 80px; background-color: #f0f0f0;">
                                      {% endif %}
                                  </button>'''

# Fix line 48 - main image (remove duplicate)
old2 = '''                                        <div class="product__details-nav-thumb w-img">
                                            <img src="{{ product.image.url }}" alt="{{ product.name }}">
                                                                                    {% if product.image %}
                                                                                        <img src="{{ product.image.url }}" alt="{{ product.name }}">
                                                                                    {% else %}
                                                                                        <img src="{% static 'assets/img/product/placeholder.jpg' %}" alt="{{ product.name }}" style="background-color: #f0f0f0; width: 100%; height: auto;">
                                                                                    {% endif %}
                                        </div>'''

new2 = '''                                        <div class="product__details-nav-thumb w-img">
                                            {% if product.image %}
                                                <img src="{{ product.image.url }}" alt="{{ product.name }}">
                                            {% else %}
                                                <img src="{% static 'assets/img/product/placeholder.jpg' %}" alt="{{ product.name }}" style="background-color: #f0f0f0; width: 100%; height: auto;">
                                            {% endif %}
                                        </div>'''

if old1 in content:
    content = content.replace(old1, new1)
    print("✓ Fixed thumbnail image (line 40)")
else:
    print("⚠️ Thumbnail pattern not found")

if old2 in content:
    content = content.replace(old2, new2)
    print("✓ Fixed main image and removed duplicate (line 48)")
else:
    print("⚠️ Main image pattern not found")

with open('Hub/templates/product-details.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ product-details.html updated")
