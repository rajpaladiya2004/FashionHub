from django.urls import path
from . import views

urlpatterns = [
    # Profile
    path('profile/', views.profile_view, name='profile'),
    
    # Cart URLs
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-quantity/<int:cart_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    
    # Wishlist URLs
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/add/<int:product_id>/', views.ajax_add_to_wishlist, name='ajax_add_to_wishlist'),
    path('remove-from-wishlist/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('move-wishlist-to-cart/<int:wishlist_id>/', views.move_wishlist_to_cart, name='move_wishlist_to_cart'),
    
    # Review URLs
    path('product/<int:product_id>/submit-review/', views.submit_review, name='submit_review'),
]