from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserProfile, Order, Cart, Wishlist, ProductReview


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create user profile when user is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Order)
def update_activity_on_order(sender, instance, created, **kwargs):
    """Update user's last activity when they place an order"""
    if created:
        try:
            profile = instance.user.userprofile
            profile.last_activity = timezone.now()
            profile.save(update_fields=['last_activity'])
        except:
            pass


@receiver(post_save, sender=Cart)
def update_activity_on_cart(sender, instance, created, **kwargs):
    """Update user's last activity when they add to cart"""
    if created:
        try:
            profile = instance.user.userprofile
            profile.last_activity = timezone.now()
            profile.save(update_fields=['last_activity'])
        except:
            pass


@receiver(post_save, sender=Wishlist)
def update_activity_on_wishlist(sender, instance, created, **kwargs):
    """Update user's last activity when they add to wishlist"""
    if created:
        try:
            profile = instance.user.userprofile
            profile.last_activity = timezone.now()
            profile.save(update_fields=['last_activity'])
        except:
            pass


@receiver(post_save, sender=ProductReview)
def update_activity_on_review(sender, instance, created, **kwargs):
    """Update user's last activity when they submit a review"""
    if created:
        try:
            profile = instance.user.userprofile
            profile.last_activity = timezone.now()
            profile.save(update_fields=['last_activity'])
        except:
            pass
