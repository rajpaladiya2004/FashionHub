#!/usr/bin/env python
"""
Add AJAX wishlist view to views.py
"""

new_view = '''

# ===== AJAX WISHLIST VIEW =====

@login_required(login_url='login')
def ajax_add_to_wishlist(request, product_id):
    """AJAX endpoint to add product to wishlist"""
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=request.user,
                product=product
            )
            
            if created:
                return JsonResponse({
                    'success': True,
                    'message': f'{product.name} added to wishlist!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': f'{product.name} is already in your wishlist'
                })
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Product not found'
            }, status=404)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
'''

with open('Hub/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add the new view before the last line
content = content.rstrip() + new_view

with open('Hub/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Added ajax_add_to_wishlist view to views.py")
