from django.urls import path
from . import views

urlpatterns = [
    # Admin Panel URLs
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/test/', views.admin_test, name='admin_test'),
    path('admin-panel/widgets/', views.admin_widgets, name='admin_widgets'),
    path('admin-panel/add-product/', views.admin_add_product, name='admin_add_product'),
    path('admin-panel/products/', views.admin_product_list, name='admin_product_list'),
    path('admin-panel/products/edit/<int:product_id>/', views.admin_edit_product, name='admin_edit_product'),
    path('admin-panel/products/delete/<int:product_id>/', views.admin_delete_product, name='admin_delete_product'),
    path('admin-panel/categories/', views.admin_categories, name='admin_categories'),
    path('admin-panel/categories/add/', views.admin_add_category, name='admin_add_category'),
    path('admin-panel/categories/edit/<int:category_id>/', views.admin_edit_category, name='admin_edit_category'),
    path('admin-panel/categories/delete/<int:category_id>/', views.admin_delete_category, name='admin_delete_category'),
    path('admin-panel/reviews/', views.admin_reviews, name='admin_reviews'),
    path('admin-panel/orders/', views.admin_orders, name='admin_orders'),
    path('admin-panel/orders/<int:order_id>/', views.admin_order_details, name='admin_order_details'),
    path('admin-panel/invoices/', views.admin_invoices, name='admin_invoices'),
    path('admin-panel/customers/', views.admin_customers, name='admin_customers'),
    path('admin-panel/customers/<int:customer_id>/', views.admin_customer_details, name='admin_customer_details'),
    path('admin-panel/banners/', views.admin_banners, name='admin_banners'),
    path('admin-panel/banners/add/', views.admin_add_banner, name='admin_add_banner'),
    path('admin-panel/banners/edit/<int:banner_id>/', views.admin_edit_banner, name='admin_edit_banner'),
    path('admin-panel/banners/delete/<int:banner_id>/', views.admin_delete_banner, name='admin_delete_banner'),
    path('admin-panel/sliders/', views.admin_sliders, name='admin_sliders'),
    path('admin-panel/sliders/add/', views.admin_add_slider, name='admin_add_slider'),
    path('admin-panel/sliders/edit/<int:slider_id>/', views.admin_edit_slider, name='admin_edit_slider'),
    path('admin-panel/sliders/delete/<int:slider_id>/', views.admin_delete_slider, name='admin_delete_slider'),
    path('admin-panel/questions/', views.admin_questions, name='admin_questions'),
    path('admin-panel/questions/<int:question_id>/approve/', views.admin_approve_question, name='admin_approve_question'),
    path('admin-panel/questions/<int:question_id>/delete/', views.admin_delete_question, name='admin_delete_question'),
    path('admin-panel/product/<int:product_id>/adjust-rating/', views.admin_adjust_rating, name='admin_adjust_rating'),
    path('admin-panel/reviews/<int:review_id>/approve/', views.admin_approve_review, name='admin_approve_review'),
    path('admin-panel/reviews/<int:review_id>/delete/', views.admin_delete_review, name='admin_delete_review'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
    
    # Cart URLs
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/toggle/<int:product_id>/', views.ajax_toggle_cart, name='ajax_toggle_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-quantity/<int:cart_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    
    # Wishlist URLs
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/add/<int:product_id>/', views.ajax_add_to_wishlist, name='ajax_add_to_wishlist'),
    path('ajax-add-to-wishlist/<int:product_id>/', views.ajax_add_to_wishlist, name='ajax_add_to_wishlist_alt'),
    path('check-wishlist/<int:product_id>/', views.check_wishlist, name='check_wishlist'),
    path('remove-from-wishlist/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('move-wishlist-to-cart/<int:wishlist_id>/', views.move_wishlist_to_cart, name='move_wishlist_to_cart'),
    
    # Buy Now & Checkout URLs
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('razorpay-payment/<int:order_id>/', views.razorpay_payment, name='razorpay_payment'),
    path('razorpay-payment-success/', views.razorpay_payment_success, name='razorpay_payment_success'),
    path('resell-order/<int:order_id>/', views.resell_order, name='resell_order'),
    
    # Order Management URLs
    path('orders/', views.order_list, name='order_list'),
    path('order/download-invoice/<str:order_number>/', views.download_invoice, name='download_invoice'),
    path('order/<str:order_number>/', views.order_details, name='order_details'),
    
    # Review URLs
    path('product/<int:product_id>/submit-review/', views.submit_review, name='submit_review'),
    path('review/<int:review_id>/vote/', views.vote_review, name='vote_review'),
    path('product/<int:product_id>/submit-question/', views.submit_question, name='submit_question'),
]