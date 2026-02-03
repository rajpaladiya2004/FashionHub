from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

class CategoryIcon(models.Model):
    """Category icons for Shop By Department section"""
    name = models.CharField(max_length=100, help_text="Category name (e.g., Mobiles, Food & Health)")
    icon_class = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="FontAwesome icon class (e.g., 'fas fa-mobile-alt') - DEPRECATED: Use icon_image instead"
    )
    icon_image = models.ImageField(
        upload_to='category_icons/',
        blank=True,
        null=True,
        help_text="Upload category icon image (PNG with transparent background recommended)"
    )
    category_key = models.CharField(
        max_length=50,
        unique=True,
        help_text="Category key matching Product.CATEGORY_CHOICES (e.g., 'MOBILES')"
    )
    background_gradient = models.CharField(
        max_length=200,
        default="linear-gradient(135deg, #e0f7ff 0%, #b3e5fc 100%)",
        help_text="CSS gradient for icon background"
    )
    icon_color = models.CharField(
        max_length=20,
        default="#0288d1",
        help_text="Icon color (hex code) - Only used for FontAwesome icons"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers appear first)")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Category Icon"
        verbose_name_plural = "Category Icons"

    def __str__(self):
        return self.name

class Slider(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='sliders/')
    top_button_text = models.CharField(max_length=50, default="HOT DEALS")
    top_button_url = models.CharField(max_length=100)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title




class Feature(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    icon_class = models.CharField(
        max_length=50,
        help_text="FontAwesome class e.g. 'fal fa-truck'"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Banner(models.Model):
    BANNER_TYPE_CHOICES = [
        ('SMALL', 'Small Banner'),
        ('MEDIUM', 'Medium Banner'),
        ('LARGE', 'Large Banner'),
    ]
    
    PAGE_CHOICES = [
        ('HOME', 'Home Page'),
        ('SHOP', 'Shop Page'),
        ('BOTH', 'Both Home & Shop'),
    ]
    
    BUTTON_STYLE_CHOICES = [
        ('st-btn', 'Yellow Button (HOT DEALS)'),
        ('st-btn-3 b-radius', 'White Button (Shop Deals)'),
        ('none', 'No Button'),
    ]
    
    title = models.CharField(max_length=200, help_text="Main title/heading of the banner")
    subtitle = models.CharField(max_length=200, blank=True, help_text="Subtitle or description (optional)")
    badge_text = models.CharField(max_length=50, blank=True, help_text="Badge text like 'HOT DEALS' (optional)")
    
    image = models.ImageField(upload_to='banners/', help_text="Banner background image")
    
    link_url = models.CharField(
        max_length=200,
        default="#",
        blank=True,
        help_text="URL to redirect when banner is clicked"
    )
    
    button_text = models.CharField(max_length=50, blank=True, help_text="Button text like 'Shop Deals' (optional)")
    button_style = models.CharField(
        max_length=20,
        choices=BUTTON_STYLE_CHOICES,
        default='none',
        help_text="Select button style"
    )
    
    banner_type = models.CharField(
        max_length=10,
        choices=BANNER_TYPE_CHOICES,
        default='LARGE',
        help_text="Banner size type"
    )
    
    page_type = models.CharField(
        max_length=10,
        choices=PAGE_CHOICES,
        default='HOME',
        help_text="Which page to display this banner on"
    )
    
    background_color = models.CharField(
        max_length=20,
        blank=True,
        help_text="Optional background color overlay (e.g., rgba(255,0,0,0.1))"
    )
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower number = shown first)")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.get_banner_type_display()}) - {self.get_page_type_display()}"


CATEGORY_CHOICES = [
    ('TOP_DEALS', 'Top Deals Of The Day'),
    ('TOP_SELLING', 'Top Selling Products'),
    ('TOP_FEATURED', 'Top Featured Products'),
    ('RECOMMENDED', 'Recommended For You'),
    ('MOBILES', 'Mobiles'),
    ('FOOD_HEALTH', 'Food & Health'),
    ('HOME_KITCHEN', 'Home & Kitchen'),
    ('AUTO_ACC', 'Auto Acc'),
    ('FURNITURE', 'Furniture'),
    ('SPORTS', 'Sports'),
    ('GENZ_TRENDS', 'GenZ Trends'),
    ('NEXT_GEN', 'Next Gen'),
]


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Stock Keeping Unit")
    image = models.ImageField(upload_to='products/')
    description = models.TextField(blank=True, help_text="Full product description")
    descriptionImage = models.ImageField(upload_to='products/descriptions/', blank=True, null=True, help_text="Large description image displayed below product description")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True
    )

    discount_percent = models.PositiveIntegerField(default=0)

    sold = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    
    # Product Details
    weight = models.CharField(max_length=50, blank=True, help_text="e.g., 2 lbs")
    dimensions = models.CharField(max_length=100, blank=True, help_text="e.g., 12 × 16 × 19 in")
    color = models.CharField(max_length=100, blank=True, help_text="Available colors")
    size = models.CharField(max_length=100, blank=True, help_text="Available sizes")
    brand = models.CharField(max_length=100, blank=True)
    shipping_info = models.CharField(max_length=200, blank=True, help_text="e.g., Standard shipping: $5.95")
    care_info = models.TextField(blank=True, help_text="Care instructions")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    
    is_top_deal = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    rating = models.FloatField(default=0)
    review_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            
            # Make slug unique by appending counter if needed
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        super().save(*args, **kwargs)

    def progress_percent(self):
        if self.stock == 0:
            return 0
        return int((self.sold / self.stock) * 100)

    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """Additional images for product gallery"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='products/gallery/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - Image {self.order}"


class ProductStockNotification(models.Model):
    """Record of users requesting restock notifications"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_notifications')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_notifications')
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    notified_at = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        unique_together = ('product', 'email')
        ordering = ['-created_at']

    def mark_sent(self):
        self.is_sent = True
        self.notified_at = timezone.now()
        self.save(update_fields=['is_sent', 'notified_at'])

    def __str__(self):
        return f"Notify {self.email} about {self.product.name}"


class DealCountdown(models.Model):
    title = models.CharField(max_length=100, default="Top Deals Of The Day")
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title




class UserProfile(models.Model):
    CUSTOMER_SEGMENT_CHOICES = [
        ('NEW', 'New Customer'),
        ('REGULAR', 'Regular Customer'),
        ('VIP', 'VIP Customer'),
        ('ADMIN', 'Admin User'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png', blank=True)
    country_code = models.CharField(max_length=5, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    is_blocked = models.BooleanField(default=False, help_text="Block user from accessing the site")
    customer_segment = models.CharField(max_length=15, choices=CUSTOMER_SEGMENT_CHOICES, default='NEW')
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    def get_orders_count(self):
        """Get total number of orders (placeholder - needs Order model)"""
        return 0
    
    def get_wishlist_count(self):
        """Get wishlist items count"""
        return self.user.wishlist_items.count()
    
    def get_cart_count(self):
        """Get cart items count"""
        return self.user.cart_items.count()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name_plural = 'Cart Items'

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x{self.quantity}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name_plural = 'Wishlist Items'

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class ProductReview(models.Model):
    """Product reviews with admin approval workflow and enhanced features"""
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    name = models.CharField(max_length=100, help_text="Reviewer name")
    email = models.EmailField()
    comment = models.TextField()
    is_approved = models.BooleanField(default=False, help_text="Admin must approve before review is publicly visible")
    is_verified_purchase = models.BooleanField(default=False, help_text="User purchased this product")
    is_auto_generated = models.BooleanField(default=False, help_text="Auto-generated review by system")
    helpful_count = models.PositiveIntegerField(default=0, help_text="Number of helpful votes")
    not_helpful_count = models.PositiveIntegerField(default=0, help_text="Number of not helpful votes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating} stars) - {'Approved' if self.is_approved else 'Pending'}"
    
    def get_helpfulness_percentage(self):
        """Calculate helpfulness percentage"""
        total_votes = self.helpful_count + self.not_helpful_count
        if total_votes == 0:
            return 0
        return int((self.helpful_count / total_votes) * 100)
    
    def save(self, *args, **kwargs):
        """Override save to auto-update product rating and review count"""
        super().save(*args, **kwargs)
        
        # Update product review count and rating
        from django.db.models import Avg
        
        product = self.product
        approved_reviews = ProductReview.objects.filter(product=product, is_approved=True)
        
        if approved_reviews.exists():
            # Update review count
            product.review_count = approved_reviews.count()
            
            # Update average rating
            avg_rating = approved_reviews.aggregate(Avg('rating'))['rating__avg']
            product.rating = round(avg_rating, 1) if avg_rating else 0
        else:
            product.review_count = 0
            product.rating = 0
        
        product.save(update_fields=['review_count', 'rating'])


class ReviewImage(models.Model):
    """Images uploaded with product reviews"""
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='reviews/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['uploaded_at']
    
    def __str__(self):
        return f"Image for {self.review.product.name} review by {self.review.user.username}"


class ReviewVote(models.Model):
    """Track user votes on review helpfulness"""
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_helpful = models.BooleanField(help_text="True for helpful, False for not helpful")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('review', 'user')
        verbose_name = 'Review Vote'
        verbose_name_plural = 'Review Votes'
    
    def __str__(self):
        vote_type = "helpful" if self.is_helpful else "not helpful"
        return f"{self.user.username} voted {vote_type} on review #{self.review.id}"


class ProductQuestion(models.Model):
    """Q&A section for products"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(help_text="Customer question")
    answer = models.TextField(blank=True, help_text="Admin answer")
    answered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='answered_questions')
    is_answered = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False, help_text="Show on product page only after admin approval and answer")
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product Question'
        verbose_name_plural = 'Product Questions'
    
    def __str__(self):
        status = "Answered" if self.is_answered else "Pending"
        return f"Q&A for {self.product.name} - {status}"


# ==================== ORDER MANAGEMENT MODELS ====================

class Address(models.Model):
    """Customer shipping and billing addresses"""
    ADDRESS_TYPE_CHOICES = [
        ('HOME', 'Home'),
        ('OFFICE', 'Office'),
        ('OTHER', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, default='HOME')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Addresses'
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.state}"
    
    def save(self, *args, **kwargs):
        # If this is set as default, unset other defaults for this user
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class Order(models.Model):
    """Customer orders"""
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment'),
        ('UPI', 'UPI'),
        ('CARD', 'Credit/Debit Card'),
    ]
    
    # Order identification
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    
    # Order amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Order status
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='COD')
    
    # Dates
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    
    # Addresses (stored as text to preserve at time of order)
    shipping_address = models.TextField()
    billing_address = models.TextField()
    
    # Additional info
    customer_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admins")
    tracking_number = models.CharField(max_length=100, blank=True)
    courier_name = models.CharField(max_length=100, blank=True, help_text="Courier/Shipping company name")
    invoice_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    
    # Payment related fields
    razorpay_order_id = models.CharField(max_length=100, blank=True, help_text="Razorpay Order ID")
    razorpay_payment_id = models.CharField(max_length=100, blank=True, help_text="Razorpay Payment ID")
    razorpay_signature = models.CharField(max_length=200, blank=True, help_text="Razorpay Payment Signature")
    
    # Resell functionality
    is_resell = models.BooleanField(default=False, help_text="Is this a resell order?")
    resell_from_name = models.CharField(max_length=200, blank=True, help_text="Original seller name for resell orders")
    resell_from_phone = models.CharField(max_length=20, blank=True, help_text="Original seller phone for resell orders")
    
    # Order Approval System
    APPROVAL_STATUS_CHOICES = [
        ('PENDING_APPROVAL', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('AUTO_APPROVED', 'Auto Approved'),
    ]
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='PENDING_APPROVAL')
    approval_notes = models.TextField(blank=True, help_text="Admin notes for approval/rejection")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_orders')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Fraud Detection Flags
    is_suspicious = models.BooleanField(default=False, help_text="Flagged as potentially fraudulent")
    suspicious_reason = models.TextField(blank=True, help_text="Reason for flagging as suspicious")
    risk_score = models.IntegerField(default=0, help_text="Fraud risk score (0-100)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate unique order number: ORD20260129001
            import datetime
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            last_order = Order.objects.filter(order_number__startswith=f'ORD{date_str}').order_by('-order_number').first()
            if last_order:
                last_number = int(last_order.order_number[-3:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.order_number = f'ORD{date_str}{new_number:03d}'
        super().save(*args, **kwargs)
    
    def get_status_color(self):
        """Return color class for order status"""
        status_colors = {
            'PENDING': 'warning',
            'PROCESSING': 'info',
            'SHIPPED': 'primary',
            'DELIVERED': 'success',
            'CANCELLED': 'danger',
        }
        return status_colors.get(self.order_status, 'secondary')
    
    def get_payment_status_color(self):
        """Return color class for payment status"""
        payment_colors = {
            'PENDING': 'warning',
            'PAID': 'success',
            'FAILED': 'danger',
            'REFUNDED': 'info',
        }
        return payment_colors.get(self.payment_status, 'secondary')
    
    def calculate_risk_score(self):
        """Calculate fraud risk score for this order"""
        risk = 0
        
        # High value order (>10000)
        if self.total_amount > 10000:
            risk += 30
        
        # Very high value (>50000)
        if self.total_amount > 50000:
            risk += 40
        
        # First time customer
        user_orders_count = Order.objects.filter(user=self.user).count()
        if user_orders_count <= 1:
            risk += 20
        
        # Multiple orders same day
        from django.utils import timezone
        today_orders = Order.objects.filter(
            user=self.user,
            created_at__date=timezone.now().date()
        ).count()
        if today_orders > 3:
            risk += 25
        
        # COD for high value
        if self.payment_method == 'COD' and self.total_amount > 5000:
            risk += 15
        
        return min(risk, 100)  # Cap at 100
    
    def check_auto_approval_eligibility(self):
        """Check if order should be auto-approved"""
        # Trusted customer (>5 successful orders)
        successful_orders = Order.objects.filter(
            user=self.user,
            order_status='DELIVERED',
            payment_status='PAID'
        ).count()
        
        if successful_orders >= 5 and self.total_amount < 15000:
            return True
        
        # Low value, paid orders
        if self.payment_status == 'PAID' and self.total_amount < 5000:
            return True
        
        return False
    
    def auto_process_approval(self):
        """Automatically approve/flag order based on rules"""
        self.risk_score = self.calculate_risk_score()
        
        # Flag suspicious orders
        if self.risk_score >= 70:
            self.is_suspicious = True
            reasons = []
            if self.total_amount > 50000:
                reasons.append("Very high order value")
            if Order.objects.filter(user=self.user).count() <= 1:
                reasons.append("First time customer")
            if self.payment_method == 'COD' and self.total_amount > 5000:
                reasons.append("High value COD order")
            self.suspicious_reason = ", ".join(reasons)
            self.approval_status = 'PENDING_APPROVAL'
        
        # Auto-approve trusted customers
        elif self.check_auto_approval_eligibility():
            self.approval_status = 'AUTO_APPROVED'
            self.approved_at = timezone.now()
            self.order_status = 'PROCESSING'
        
        else:
            self.approval_status = 'PENDING_APPROVAL'
        
        self.save()


class OrderItem(models.Model):
    """Items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    # Product details at time of order (preserved even if product changes)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.CharField(max_length=500, blank=True)
    
    # Order details
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=50, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity} - Order #{self.order.order_number}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate subtotal
        self.subtotal = self.product_price * self.quantity
        super().save(*args, **kwargs)


class OrderStatusHistory(models.Model):
    """Track order status changes over time"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Order Status Histories"
    
    def __str__(self):
        return f"Order #{self.order.order_number} - {self.old_status} → {self.new_status}"


class AdminEmailSettings(models.Model):
    """Configurable admin email settings"""
    setting_name = models.CharField(max_length=100, default="order_notifications")
    admin_email = models.EmailField(default="rajpaladiya2023@gmail.com", help_text="Email to receive order notifications")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Admin Email Settings"
    
    def __str__(self):
        return f"Admin Email: {self.admin_email}"


class BrandPartner(models.Model):
    """Brand Partner logos for homepage carousel"""
    name = models.CharField(max_length=100, help_text="Brand name")
    logo = models.ImageField(upload_to='brand_partners/', help_text="Brand logo image")
    link_url = models.URLField(blank=True, null=True, help_text="Optional link URL")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    is_active = models.BooleanField(default=True, help_text="Show/hide brand")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Brand Partner"
        verbose_name_plural = "Brand Partners"
    
    def __str__(self):
        return self.name


# ============================================
# NEW FEATURES - Order Management Extensions
# ============================================

class LoyaltyPoints(models.Model):
    """Customer loyalty points system"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='loyalty_points')
    total_points = models.IntegerField(default=0, help_text="Total points earned")
    points_used = models.IntegerField(default=0, help_text="Points redeemed")
    points_available = models.IntegerField(default=0, help_text="Available points to use")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Loyalty Points"
    
    def __str__(self):
        return f"{self.user.username} - {self.points_available} points"
    
    def add_points(self, points, description=""):
        """Add points to user account"""
        self.total_points += points
        self.points_available += points
        self.save()
        
        # Create transaction record
        PointsTransaction.objects.create(
            user=self.user,
            points=points,
            transaction_type='EARNED',
            description=description
        )
    
    def redeem_points(self, points, description=""):
        """Redeem points from user account"""
        if self.points_available >= points:
            self.points_used += points
            self.points_available -= points
            self.save()
            
            # Create transaction record
            PointsTransaction.objects.create(
                user=self.user,
                points=points,
                transaction_type='REDEEMED',
                description=description
            )
            return True
        return False


class PointsTransaction(models.Model):
    """History of loyalty points transactions"""
    TRANSACTION_TYPES = [
        ('EARNED', 'Points Earned'),
        ('REDEEMED', 'Points Redeemed'),
        ('EXPIRED', 'Points Expired'),
        ('ADJUSTED', 'Manual Adjustment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points_transactions')
    points = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='points_transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Points Transaction"
        verbose_name_plural = "Points Transactions"
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} {self.points} points"


class ReturnRequest(models.Model):
    """Product return requests"""
    RETURN_REASONS = [
        ('DEFECTIVE', 'Defective/Damaged Product'),
        ('WRONG_ITEM', 'Wrong Item Received'),
        ('NOT_AS_DESCRIBED', 'Not As Described'),
        ('SIZE_ISSUE', 'Size/Fit Issue'),
        ('QUALITY_ISSUE', 'Quality Issue'),
        ('CHANGED_MIND', 'Changed Mind'),
        ('OTHER', 'Other Reason'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('PICKUP_SCHEDULED', 'Pickup Scheduled'),
        ('PICKED_UP', 'Picked Up'),
        ('REFUND_INITIATED', 'Refund Initiated'),
        ('REFUND_COMPLETED', 'Refund Completed'),
    ]
    
    return_number = models.CharField(max_length=20, unique=True, editable=False)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='return_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='return_requests')
    order_item = models.ForeignKey('OrderItem', on_delete=models.CASCADE, related_name='return_requests')
    
    reason = models.CharField(max_length=30, choices=RETURN_REASONS)
    description = models.TextField(help_text="Detailed description of the issue")
    images = models.ImageField(upload_to='returns/', blank=True, null=True, help_text="Upload product images")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(blank=True, help_text="Internal admin notes")
    
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    refund_method = models.CharField(max_length=50, blank=True, help_text="Bank transfer, Original payment method, etc.")
    
    pickup_date = models.DateTimeField(null=True, blank=True)
    refund_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Return Request"
        verbose_name_plural = "Return Requests"
    
    def __str__(self):
        return f"Return #{self.return_number} - Order #{self.order.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.return_number:
            # Generate unique return number: RET-YYYYMMDD-XXXXX
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_return = ReturnRequest.objects.filter(
                return_number__startswith=f'RET-{date_str}'
            ).order_by('-return_number').first()
            
            if last_return:
                last_num = int(last_return.return_number.split('-')[-1])
                new_num = str(last_num + 1).zfill(5)
            else:
                new_num = '00001'
            
            self.return_number = f'RET-{date_str}-{new_num}'
        
        super().save(*args, **kwargs)


class WishlistPriceAlert(models.Model):
    """Track price changes for wishlist items"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='price_alerts')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='price_alerts')
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    target_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Alert when price drops below this")
    is_active = models.BooleanField(default=True)
    notified = models.BooleanField(default=False, help_text="Has user been notified of price drop?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Wishlist Price Alert"
        verbose_name_plural = "Wishlist Price Alerts"
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Notification(models.Model):
    """User notifications"""
    NOTIFICATION_TYPES = [
        ('ORDER_PLACED', 'Order Placed'),
        ('ORDER_CONFIRMED', 'Order Confirmed'),
        ('ORDER_SHIPPED', 'Order Shipped'),
        ('ORDER_DELIVERED', 'Order Delivered'),
        ('PRICE_DROP', 'Price Drop Alert'),
        ('STOCK_AVAILABLE', 'Stock Available'),
        ('RETURN_APPROVED', 'Return Approved'),
        ('REFUND_PROCESSED', 'Refund Processed'),
        ('POINTS_EARNED', 'Loyalty Points Earned'),
        ('SPECIAL_OFFER', 'Special Offer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True, help_text="URL to related page")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
    
    def __str__(self):
        return f"{self.user.username} - {self.notification_type}"


class EmailLog(models.Model):
    """Log of sent emails"""
    EMAIL_TYPES = [
        ('ORDER_CONFIRMATION', 'Order Confirmation'),
        ('ORDER_STATUS_UPDATE', 'Order Status Update'),
        ('DELIVERY_REMINDER', 'Delivery Reminder'),
        ('REVIEW_REQUEST', 'Review Request'),
        ('PRICE_ALERT', 'Price Alert'),
        ('PROMOTIONAL', 'Promotional Email'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_logs', null=True, blank=True)
    email_to = models.EmailField()
    email_type = models.CharField(max_length=30, choices=EMAIL_TYPES)
    subject = models.CharField(max_length=300)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='email_logs')
    sent_successfully = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-sent_at']
        verbose_name = "Email Log"
        verbose_name_plural = "Email Logs"
    
    def __str__(self):
        return f"{self.email_type} to {self.email_to}"


class SiteSettings(models.Model):
    """Global site settings - only one instance should exist"""
    site_name = models.CharField(max_length=100, default='VibeMall', help_text='Website name displayed across the site')
    site_name_html = models.TextField(blank=True, help_text='Optional styled HTML for brand name (supports multiple colors/fonts)')
    site_logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Main logo (recommended: 150x50px PNG with transparent background)')
    site_favicon = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Favicon icon (recommended: 32x32px PNG)')
    tagline = models.CharField(max_length=200, blank=True, help_text='Website tagline/slogan')
    
    # Contact Information
    contact_email = models.EmailField(default='support@vibemall.com')
    contact_phone = models.CharField(max_length=20, default='+91 1234567890')
    
    # Social Media Links
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Admin Panel Logo
    admin_logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Admin panel logo (recommended: 120x40px)')
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return f"{self.site_name} Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            # Update existing instance instead of creating new
            existing = SiteSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get or create site settings"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
