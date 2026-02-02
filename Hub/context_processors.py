"""
Context processors for FashioHub
Adds cart and wishlist counts to every template
"""
from .models import Cart, Wishlist, SiteSettings, LoyaltyPoints
from django.db.models import F, Sum


def cart_wishlist_context(request):
    """Add cart and wishlist counts and totals to template context"""
    context = {
        'cart_count': 0,
        'wishlist_count': 0,
        'cart_total': 0,
        'cart_items': [],
        'loyalty_points': 0,
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
        
        # Loyalty points
        try:
            loyalty = LoyaltyPoints.objects.get(user=request.user)
            context['loyalty_points'] = loyalty.points_available
        except LoyaltyPoints.DoesNotExist:
            # Create loyalty points account if doesn't exist
            loyalty = LoyaltyPoints.objects.create(user=request.user)
            context['loyalty_points'] = 0
    
    return context


def site_settings_context(request):
    """Add site settings to every template"""
    try:
        site_settings = SiteSettings.get_settings()
    except:
        # If table doesn't exist yet (during migrations)
        site_settings = None
    
    return {
        'site_settings': site_settings,
    }
