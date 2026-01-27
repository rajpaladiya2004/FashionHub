from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Slider, Feature, Banner, Product, DealCountdown, UserProfile, Cart, Wishlist, ProductImage, ProductReview

def index(request):
    sliders = Slider.objects.filter(is_active=True)
    features = Feature.objects.filter(is_active=True)
    banners = Banner.objects.filter(is_active=True)
    top_deals = Product.objects.filter(is_active=True, category='TOP_DEALS')
    top_selling = Product.objects.filter(is_active=True, category='TOP_SELLING')
    top_featured = Product.objects.filter(is_active=True, category='TOP_FEATURED')
    recommended = Product.objects.filter(is_active=True, category='RECOMMENDED')
    countdown = DealCountdown.objects.filter(is_active=True).first()

    return render(
        request,
        'index.html',
        {
            'sliders': sliders,
            'features': features,
            'banners': banners,
            'top_deals': top_deals,
            'top_selling': top_selling,
            'top_featured': top_featured,
            'recommended': recommended,
            'countdown': countdown,
        }
    )










def about(request): return render(request, 'about.html')
def blog(request): return render(request, 'blog.html')
def blog_details(request): return render(request, 'blog-details.html')


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    total_price = sum(item.get_total_price() for item in cart_items)
    cart_count = cart_items.count()
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count
    })



def checkout(request): return render(request, 'checkout.html')
def contact(request): return render(request, 'contact.html')
def faq(request): return render(request, 'faq.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")  # change if needed
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")




def my_account(request): return render(request, 'profile.html')
def product(request): return render(request, 'product.html')
def product_details(request, product_id=None):
    """Display product details with dynamic data"""
    if product_id:
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            in_wishlist = False
            if request.user.is_authenticated:
                in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
            
            # Get approved reviews for this product
            approved_reviews = ProductReview.objects.filter(product=product, is_approved=True).select_related('user')
            review_count = approved_reviews.count()
            
            # Calculate average rating
            if review_count > 0:
                avg_rating = sum(review.rating for review in approved_reviews) / review_count
            else:
                avg_rating = product.rating
            
            return render(request, 'product-details.html', {
                'product': product,
                'in_wishlist': in_wishlist,
                'reviews': approved_reviews,
                'review_count': review_count,
                'avg_rating': avg_rating,
            })
        except Product.DoesNotExist:
            return render(request, '404.html', status=404)
    else:
        # Fallback: show first product if no ID provided
        product = Product.objects.filter(is_active=True).first()
        if product:
            in_wishlist = False
            if request.user.is_authenticated:
                in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
            
            approved_reviews = ProductReview.objects.filter(product=product, is_approved=True).select_related('user')
            review_count = approved_reviews.count()
            
            if review_count > 0:
                avg_rating = sum(review.rating for review in approved_reviews) / review_count
            else:
                avg_rating = product.rating
            
            return render(request, 'product-details.html', {
                'product': product,
                'in_wishlist': in_wishlist,
                'reviews': approved_reviews,
                'review_count': review_count,
                'avg_rating': avg_rating,
            })
        return render(request, '404.html', status=404)
def shop(request):
    products = Product.objects.filter(is_active=True)

    # Filters from query params
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')

    if category:
        products = products.filter(category=category)
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    if min_rating:
        try:
            products = products.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

    special_offers = Product.objects.filter(is_active=True).order_by('-discount_percent', '-id')[:5]

    # Category counts for sidebar
    category_counts = (
        Product.objects.filter(is_active=True)
        .values('category')
        .annotate(total=Count('id'))
    )
    category_count_map = {item['category']: item['total'] for item in category_counts}
    category_data = [
        (value, label, category_count_map.get(value, 0))
        for value, label in Product.CATEGORY_CHOICES
    ]

    wishlist_product_ids = set()
    if request.user.is_authenticated:
        wishlist_product_ids = set(
            Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        )

    # Pagination - 16 products per page (4 columns x 4 rows)
    paginator = Paginator(products, 16)
    page = request.GET.get('page', 1)
    
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    return render(request, 'shop.html', {
        'products': products_page,
        'special_offers': special_offers,
        'category_data': category_data,
        'selected_category': category,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'selected_rating': min_rating or '',
        'wishlist_product_ids': wishlist_product_ids,
    })
def shop_details(request): return render(request, 'shop-details.html')


@login_required(login_url='login')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    wishlist_count = wishlist_items.count()
    
    return render(request, 'wishlist.html', {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_count
    })

def page_404(request): return render(request, '404.html', status=404)
def order_tracking(request):return render(request, 'order-tracking.html')



def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        country_code = request.POST.get("country_code")
        mobile_number = request.POST.get("mobile_number")
        profile_image = request.FILES.get("profile_image")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.first_name = name
        user.save()

        profile = user.userprofile
        profile.country_code = country_code
        profile.mobile_number = mobile_number
        if profile_image:
            profile.profile_image = profile_image
        profile.save()


        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect("index")


# ===== CART MANAGEMENT VIEWS =====

@login_required(login_url='login')
@require_POST
def add_to_cart(request):
    """Add product to cart or increase quantity"""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f"{product.name} added to cart!")
        return redirect('cart')
    except Product.DoesNotExist:
        messages.error(request, "Product not found")
        return redirect('shop')


@login_required(login_url='login')
def remove_from_cart(request, cart_id):
    """Remove product from cart"""
    try:
        cart_item = Cart.objects.get(id=cart_id, user=request.user)
        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f"{product_name} removed from cart!")
    except Cart.DoesNotExist:
        messages.error(request, "Item not found in cart")
    
    return redirect('cart')


@login_required(login_url='login')
@require_POST
def update_cart_quantity(request, cart_id):
    """Update cart item quantity"""
    try:
        quantity = int(request.POST.get('quantity', 1))
        cart_item = Cart.objects.get(id=cart_id, user=request.user)
        
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, "Item removed from cart")
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Quantity updated")
    except (Cart.DoesNotExist, ValueError):
        messages.error(request, "Error updating quantity")
    
    return redirect('cart')


# ===== WISHLIST MANAGEMENT VIEWS =====

@login_required(login_url='login')
@require_POST
def add_to_wishlist(request):
    """Add product to wishlist"""
    product_id = request.POST.get('product_id')
    
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if created:
            messages.success(request, f"{product.name} added to wishlist!")
        else:
            messages.info(request, f"{product.name} is already in your wishlist")
        
        return redirect('wishlist')
    except Product.DoesNotExist:
        messages.error(request, "Product not found")
        return redirect('shop')


@login_required(login_url='login')
def remove_from_wishlist(request, wishlist_id):
    """Remove product from wishlist"""
    try:
        wishlist_item = Wishlist.objects.get(id=wishlist_id, user=request.user)
        product_name = wishlist_item.product.name
        wishlist_item.delete()
        messages.success(request, f"{product_name} removed from wishlist!")
    except Wishlist.DoesNotExist:
        messages.error(request, "Item not found in wishlist")
    
    return redirect('wishlist')


@login_required(login_url='login')
def move_wishlist_to_cart(request, wishlist_id):
    """Move item from wishlist to cart"""
    try:
        wishlist_item = Wishlist.objects.get(id=wishlist_id, user=request.user)
        product = wishlist_item.product
        
        # Add to cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        
        # Remove from wishlist
        wishlist_item.delete()
        
        messages.success(request, f"{product.name} moved to cart!")
    except Wishlist.DoesNotExist:
        messages.error(request, "Item not found in wishlist")
    
    return redirect('cart')


@login_required(login_url='login')
@require_POST
def submit_review(request, product_id):
    """Submit a product review (requires admin approval)"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        
        rating = int(request.POST.get('rating', 5))
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        comment = request.POST.get('comment', '').strip()
        
        if not all([name, email, comment]):
            messages.error(request, "Please fill in all required fields.")
            return redirect('product-details', product_id=product_id)
        
        # Create review (not approved by default)
        ProductReview.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            name=name,
            email=email,
            comment=comment,
            is_approved=False  # Admin must approve
        )
        
        messages.success(request, "Thank you for your review! It will be visible after admin approval.")
        
    except Product.DoesNotExist:
        messages.error(request, "Product not found")
    except ValueError:
        messages.error(request, "Invalid rating value")
    
    return redirect('product-details', product_id=product_id)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile

@login_required(login_url='login')
def profile_view(request):

    if request.method == "POST":
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")

        profile.country_code = request.POST.get("country_code")
        profile.mobile_number = request.POST.get("mobile_number")

        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES.get("profile_image")

        request.user.save()
        profile.save()

        messages.success(request, "Profile saved successfully")

        # 🔥 THIS LINE IS REQUIRED
        return redirect('profile')

    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})





# Add this to the end of views.py

@login_required(login_url='login')
def add_product(request):
    # Check if user is admin (username = 'admin')
    if request.user.username != 'FashionHub':
        messages.error(request, 'Access denied. Only FashionHub user can add products.')
        return redirect('index')
    
    if request.method == 'POST':
        try:
            # Get basic form data
            name = request.POST.get('name')
            price = request.POST.get('price')
            old_price = request.POST.get('old_price')
            stock = request.POST.get('stock')
            category = request.POST.get('category')
            rating = request.POST.get('rating', 0)
            review_count = request.POST.get('review_count', 0)
            is_active = request.POST.get('is_active') == 'on'
            is_top_deal = request.POST.get('is_top_deal') == 'on'
            
            # Get new fields
            sku = request.POST.get('sku', '')
            brand = request.POST.get('brand', '')
            tags = request.POST.get('tags', '')
            description = request.POST.get('description', '')
            weight = request.POST.get('weight', '')
            dimensions = request.POST.get('dimensions', '')
            color = request.POST.get('color', '')
            size = request.POST.get('size', '')
            shipping_info = request.POST.get('shipping_info', '')
            care_info = request.POST.get('care_info', '')
            
            # Get images
            image = request.FILES.get('image')
            gallery_images = request.FILES.getlist('gallery_images')
            
            # Create product
            product = Product.objects.create(
                name=name,
                price=price,
                old_price=old_price if old_price else None,
                stock=stock,
                category=category if category else None,
                rating=rating,
                review_count=review_count,
                is_active=is_active,
                is_top_deal=is_top_deal,
                image=image,
                sku=sku,
                brand=brand,
                tags=tags,
                description=description,
                weight=weight,
                dimensions=dimensions,
                color=color,
                size=size,
                shipping_info=shipping_info,
                care_info=care_info
            )
            
            # Add gallery images if provided
            for idx, gallery_image in enumerate(gallery_images, start=1):
                ProductImage.objects.create(
                    product=product,
                    image=gallery_image,
                    order=idx,
                    is_active=True
                )
            
            messages.success(request, f'Product "{product.name}" added successfully with {len(gallery_images)} gallery images!')
            return redirect('add_product')
            
        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')
    
    # Get all products for display
    products = Product.objects.all().order_by('-id')[:10]
    
    return render(request, 'add_product.html', {'products': products})

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
