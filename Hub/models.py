from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Slider(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='sliders/')
    top_button_text = models.CharField(max_length=50, default="HOT DEALS")
    top_button_url = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

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
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)

    image = models.ImageField(upload_to='banners/')

    link_url = models.CharField(
        max_length=200,
        default="#",
        blank=True
    )

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('TOP_DEALS', 'Top Deals Of The Day'),
        ('TOP_SELLING', 'Top Selling Products'),
        ('TOP_FEATURED', 'Top Featured Products'),
        ('RECOMMENDED', 'Recommended For You'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Stock Keeping Unit")
    image = models.ImageField(upload_to='products/')
    description = models.TextField(blank=True, help_text="Full product description")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    discount_percent = models.PositiveIntegerField(default=0)

    sold = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True,
        help_text="Select product category for homepage sections"
    )
    
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
            self.slug = slugify(self.name)
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


class DealCountdown(models.Model):
    title = models.CharField(max_length=100, default="Top Deals Of The Day")
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png', blank=True)
    country_code = models.CharField(max_length=5, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username


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
    """Product reviews with admin approval workflow"""
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating} stars) - {'Approved' if self.is_approved else 'Pending'}"
