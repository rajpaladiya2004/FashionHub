from django.core.management.base import BaseCommand
from django.db.models import Count, Q
from Hub.models import Product, Order, OrderItem, Wishlist
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Auto-update product categories based on sales, discounts, and popularity'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting automatic product categorization...')
        
        # 1. TOP_SELLING - Top 20 sold products
        top_selling = Product.objects.filter(
            is_active=True,
            sold__gt=0
        ).order_by('-sold')[:20]
        
        # Clear existing TOP_SELLING
        Product.objects.filter(category='TOP_SELLING').update(category=None)
        
        for product in top_selling:
            product.category = 'TOP_SELLING'
            product.save(update_fields=['category'])
        
        self.stdout.write(f'✓ Updated {top_selling.count()} TOP_SELLING products')
        
        # 2. TOP_DEALS - Top 20 discount products (highest discount_percent)
        top_deals = Product.objects.filter(
            is_active=True,
            discount_percent__gt=0
        ).order_by('-discount_percent')[:20]
        
        # Clear existing TOP_DEALS
        Product.objects.filter(category='TOP_DEALS').update(category=None)
        
        for product in top_deals:
            product.category = 'TOP_DEALS'
            product.save(update_fields=['category'])
        
        self.stdout.write(f'✓ Updated {top_deals.count()} TOP_DEALS products')
        
        # 3. RECOMMENDED - Most wishlisted products (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        recommended_products = Product.objects.filter(
            is_active=True,
            wishlist__created_at__gte=thirty_days_ago
        ).annotate(
            wishlist_count=Count('wishlist')
        ).order_by('-wishlist_count')[:20]
        
        # Clear existing RECOMMENDED
        Product.objects.filter(category='RECOMMENDED').update(category=None)
        
        for product in recommended_products:
            product.category = 'RECOMMENDED'
            product.save(update_fields=['category'])
        
        self.stdout.write(f'✓ Updated {recommended_products.count()} RECOMMENDED products')
        
        # 4. TOP_FEATURED - Highest rated products with reviews
        top_featured = Product.objects.filter(
            is_active=True,
            rating__gte=4.0,
            review_count__gte=5
        ).order_by('-rating', '-review_count')[:20]
        
        # Clear existing TOP_FEATURED
        Product.objects.filter(category='TOP_FEATURED').update(category=None)
        
        for product in top_featured:
            product.category = 'TOP_FEATURED'
            product.save(update_fields=['category'])
        
        self.stdout.write(f'✓ Updated {top_featured.count()} TOP_FEATURED products')
        
        self.stdout.write(self.style.SUCCESS('✓ Product categorization completed successfully!'))
