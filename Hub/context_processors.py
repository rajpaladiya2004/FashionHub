"""
Context processors for FashioHub
Adds cart and wishlist counts to every template
"""
from .models import Cart, Wishlist
from django.db.models import F, Sum


def cart_wishlist_context(request):
    """Add cart and wishlist counts and totals to template context"""
    context = {
        'cart_count': 0,
        'wishlist_count': 0,
        'cart_total': 0,
        'cart_items': [],
    }
    
    if request.user.is_authenticated:
        # Cart items and count
        cart_items = Cart.objects.filter(user=request.user).select_related('product')
        context['cart_count'] = cart_items.count()
        context['cart_items'] = cart_items
        
        # Calculate cart total
        cart_total = sum(item.get_total_price() for item in cart_items)
        context['cart_total'] = f"{cart_total:.2f}"
        
        # Wishlist count
        context['wishlist_count'] = Wishlist.objects.filter(user=request.user).count()
    
    return context
