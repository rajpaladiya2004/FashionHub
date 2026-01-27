import os

content = """# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Slider, Feature, Banner, Product, DealCountdown, Cart, Wishlist

admin.site.register(Slider)

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_class', 'order', 'is_active')
    list_editable = ('order', 'is_active')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'old_price', 'discount_percent', 'stock', 'category', 'rating', 'is_active', 'image_thumbnail')
    list_filter = ('category', 'is_active', 'is_top_deal')
    list_editable = ('category', 'is_active', 'price', 'stock')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'id', 'slug')
    readonly_fields = ('slug', 'image_preview')
    
    fieldsets = (
        ('BASIC INFORMATION', {
            'fields': ('name', 'slug', 'category', 'is_active', 'is_top_deal'),
            'description': 'Product name, category, and status'
        }),
        ('PRODUCT IMAGE', {
            'fields': ('image', 'image_preview'),
            'description': 'Upload a product image (JPEG/PNG, recommended size: 400x400px)'
        }),
        ('PRICING', {
            'fields': ('price', 'old_price', 'discount_percent'),
            'description': 'Set price, old price (for comparison), and discount percentage'
        }),
        ('INVENTORY', {
            'fields': ('stock', 'sold'),
            'description': 'Stock quantity and units sold'
        }),
        ('RATINGS & REVIEWS', {
            'fields': ('rating', 'review_count'),
            'description': 'Product rating (0-5) and number of reviews'
        }),
    )
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 5px; object-fit: cover;" />',
                obj.image.url
            )
        return '-'
    image_thumbnail.short_description = 'Image'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; height: auto; border-radius: 8px; border: 1px solid #ddd; padding: 10px;" />',
                obj.image.url
            )
        return 'No image uploaded yet'
    image_preview.short_description = 'Image Preview'
    
    def save_model(self, request, obj, form, change):
        if obj.old_price and obj.price:
            discount = ((obj.old_price - obj.price) / obj.old_price) * 100
            if not obj.discount_percent or obj.discount_percent == 0:
                obj.discount_percent = int(discount)
        super().save_model(request, obj, form, change)

@admin.register(DealCountdown)
class DealCountdownAdmin(admin.ModelAdmin):
    list_display = ('title', 'end_time', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'added_at')
    list_filter = ('user', 'added_at')
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('added_at', 'updated_at')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'added_at')
    list_filter = ('user', 'added_at')
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('added_at',)
"""

with open('Hub/admin.py', 'w') as f:
    f.write(content)

print("✓ admin.py updated successfully with enhanced product management interface!")
