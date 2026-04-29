from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductForm
from .models import Product, UserProfile, Order, Cart, CartItem, Category
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
try:
    import google.generativeai as genai
except ImportError:
    genai = None

import os


def home(request):
    featured_products = Product.objects.filter(
        is_featured=True).order_by('-created_at')[:4]
    new_arrivals = Product.objects.filter(
        is_new=True).order_by('-created_at')[:4]
    context = {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def faq(request):
    return render(request, 'faq.html')


def admin_check(user):
    return user.is_superuser


def shop(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'shop.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


def sign_in(request):
    next_url = request.GET.get('next', 'buyer_dashboard')
    if request.user.is_authenticated:
        return redirect(next_url)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.POST.get('next', 'buyer_dashboard')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect(next_url)
        else:
            messages.error(
                request, "Invalid email or password. Please try again.")

    return render(request, 'sign_in.html')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('buyer_dashboard')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():
            messages.error(
                request, "An account with this email already exists.")
            return render(request, 'sign_in.html', {'mode': 'signup'})

        try:
            # Create user with email as username
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            # Create UserProfile
            UserProfile.objects.create(user=user, points=500, tier='Elite')

            login(request, user)
            messages.success(
                request, "Membership confirmed! Welcome to LuxeHairs.")
            next_url = request.POST.get('next', 'buyer_dashboard')
            return redirect(next_url)
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")

    return render(request, 'sign_in.html', {'mode': 'signup'})


def sign_out(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect('home')


@login_required
def buyer_dashboard(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Handle Profile Update
    if request.method == 'POST':
        # Update User fields
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()

        # Update Profile fields
        profile.phone_number = request.POST.get('phone', profile.phone_number)
        birth = request.POST.get('birth_date')
        if birth:
            profile.birth_date = birth

        profile.face_shape = request.POST.get('face_shape', profile.face_shape)
        profile.lustre_bias = request.POST.get(
            'lustre_bias', profile.lustre_bias)

        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']

        profile.save()
        messages.success(request, "Your signature identity has been updated.")
        return redirect('buyer_dashboard')

    # Fetch orders
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Stats
    total_orders = orders.count()
    active_orders = orders.filter(
        status__in=['Pending', 'Processing', 'In Transit']).count()

    # Tier Calculation
    # Logic: Member -> (15,000) -> Gold -> (40,000) -> Platinum
    current_points = profile.points
    tier_target = 15000
    next_tier = "Gold"

    if current_points >= 40000:
        tier_target = 100000  # Arbitrary high number for max tier
        next_tier = "Diamond"
    elif current_points >= 15000:
        tier_target = 40000
        next_tier = "Platinum"

    progress_percent = min(int((current_points / tier_target) * 100), 100)
    points_needed = max(tier_target - current_points, 0)

    context = {
        'profile': profile,
        'orders': orders,
        'total_orders': total_orders,
        'active_orders': active_orders,
        'wishlist': [],
        'tier_progress': progress_percent,
        'points_needed': points_needed,
        'next_tier': next_tier,
        'tier_target': tier_target
    }
    return render(request, 'buyer_dashboard.html', context)


@login_required
def cart(request):
    try:
        cart_obj = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart_obj = Cart.objects.create(user=request.user)

    return render(request, 'cart.html', {'cart': cart_obj})


@login_required
def add_to_cart(request, product_id):
    cart_obj, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart_obj, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to your bag.")
    return redirect('shop')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from your bag.")
    return redirect('cart')


@login_required
def update_cart_quantity(request, item_id, action):
    cart_item = get_object_or_404(
        CartItem, id=item_id, cart__user=request.user)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity -= 1

    if cart_item.quantity <= 0:
        cart_item.delete()
    else:
        cart_item.save()

    return redirect('cart')


def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # --- AI Integration (Primary) ---
            api_key = os.environ.get('GEMINI_API_KEY')

            if api_key and genai:
                try:
                    # Configure Gemini
                    genai.configure(api_key=api_key)
                    
                    # Persona & Context (Optimized as System Instruction)
                    system_prompt = (
                        "You are Luxie, the boutique AI concierge for LuxeHairs, a premium luxury wig brand. "
                        "Your tone is sophisticated, inviting, and professional yet warm (e.g., use terms like 'Hun', 'Gorgeous', 'Darling' sparingly). "
                        "You help clients with: \n"
                        "1. Product Info: Premium wigs (Silk Base, Lace Front) starting ~$250. High-quality Virgin & Raw hair. \n"
                        "2. Services: Custom hairline customization, bleaching knots. \n"
                        "3. Logistics: Worldwide shipping (Standard 3-5 days, Express 1-2 days). Returns accepted on unworn items within 14 days. \n"
                        "4. Advice: Provide expert hair care tips for longevity. \n"
                        "If you are unsure of specific stock, ask them to check the 'Shop' page or contact a human agent. "
                        "Keep your answers short, concise, helpful, and elegant. "
                    )

                    model = genai.GenerativeModel(
                        model_name='gemini-1.5-flash',
                        system_instruction=system_prompt
                    )

                    # Generate content directly (Faster for stateless chat)
                    response = model.generate_content(user_message)
                    
                    if response and response.text:
                        return JsonResponse({'response': response.text})
                    else:
                        raise Exception("Empty response from Gemini")

                except Exception as e:
                    # Log error to console for debugging
                    print(f"--- Luxie AI Error Details ---")
                    print(f"Error: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    print(f"------------------------------")
                    pass

            # --- Rule-Based Fallback (Secondary) ---
            user_message = user_message.lower()

            if 'hello' in user_message or 'hi' in user_message:
                response = "Hello gorgeous! How can Luxie help you today? ✨"
            elif 'wig' in user_message or 'style' in user_message:
                response = "We have a stunning collection of luxury wigs! Would you like to see our 'Silk Base' or 'Lace Front' collection? 🎀"
            elif 'price' in user_message or 'cost' in user_message:
                response = "Our premium wigs start from $250. You can check the 'Shop' section for detailed pricing on each piece! 💎"
            elif 'order' in user_message or 'track' in user_message:
                response = "I can help with that! Please provide your order number, or sign in to your dashboard to see your latest status. 🚚"
            elif 'shipping' in user_message or 'delivery' in user_message:
                response = "We offer premium worldwide shipping! Standard delivery takes 3-5 business days, while express delivery takes 1-2 business days. ✈️"
            elif 'return' in user_message or 'refund' in user_message:
                response = "We want you to love your hair! If you're not satisfied, we offer returns on unworn items in their original packaging within 14 days. 🛍️"
            elif 'payment' in user_message:
                response = "We accept all major credit cards, PayPal, and Apple Pay. Your transaction is always safe and secure with us! 💳"
            elif 'okay' in user_message or 'thanks' in user_message:
                response = "You're welcome! Is there anything else I can help you with? 💖"
            elif 'bye' in user_message or 'goodbye' in user_message:
                response = "Goodbye! Have a great day! 💖"
            else:
                response = "That's a great question! I'm still learning about all our fabulous products. Would you like to speak with a human stylist, or should I try to find more info for you? 💖"

            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@user_passes_test(admin_check)
def custom_admin(request):
    from django.db.models import Count

    products = Product.objects.all().order_by('-created_at')
    users = User.objects.all().order_by('-date_joined')
    orders = Order.objects.all().order_by('-created_at')

    # Basic Stats
    total_products = products.count()
    featured_count = products.filter(is_featured=True).count()
    total_orders = orders.count()
    total_users = users.count()

    # Order Statistics
    pending_orders = orders.filter(status='pending').count()
    processing_orders = orders.filter(status='processing').count()
    completed_orders = orders.filter(status='completed').count()
    cancelled_orders = orders.filter(status='cancelled').count()

    # Revenue Metrics
    total_revenue = sum(
        order.total_price for order in orders.filter(status='completed'))
    pending_revenue = sum(
        order.total_price for order in orders.filter(status='pending'))
    average_order_value = total_revenue / \
        completed_orders if completed_orders > 0 else 0

    # Site Performance
    categories = Category.objects.all()
    total_categories = categories.count()

    # Top category (most products)
    top_category = categories.annotate(product_count=Count(
        'products')).order_by('-product_count').first()
    top_category_name = top_category.name if top_category else "N/A"

    # Best selling product (approximation - you may want to track actual sales)
    best_selling_product = products.filter(is_bestseller=True).first()
    best_selling_name = best_selling_product.name if best_selling_product else "N/A"

    # Conversion rate (completed orders / total users)
    conversion_rate = (completed_orders / total_users *
                       100) if total_users > 0 else 0

    context = {
        'total_products': total_products,
        'featured_count': featured_count,
        'total_orders': total_orders,
        'total_users': total_users,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'total_revenue': total_revenue,
        'pending_revenue': pending_revenue,
        'average_order_value': average_order_value,
        'total_categories': total_categories,
        'top_category': top_category_name,
        'best_selling_product': best_selling_name,
        'conversion_rate': conversion_rate,
    }
    return render(request, 'admin.html', context)


@user_passes_test(admin_check)
def admin_customers(request):
    users = User.objects.all().order_by('-date_joined')
    total_users = users.count()

    context = {
        'users': users,
        'total_users': total_users
    }
    return render(request, 'admin_customers.html', context)


@user_passes_test(admin_check)
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')

    # Order statistics
    total_orders = orders.count()
    pending_orders = orders.filter(status='pending').count()
    processing_orders = orders.filter(status='processing').count()
    completed_orders = orders.filter(status='completed').count()

    # Calculate total revenue from completed orders
    total_revenue = sum(
        order.total_price for order in orders.filter(status='completed'))

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'completed_orders': completed_orders,
        'total_revenue': total_revenue,
    }
    return render(request, 'admin_orders.html', context)


@user_passes_test(admin_check)
def admin_inventory(request):
    products = Product.objects.all().order_by('-created_at')

    context = {
        'products': products,
    }
    return render(request, 'admin_inventory.html', context)


@user_passes_test(admin_check)
def admin_product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Product added successfully to the boutique.")
            return redirect('custom_admin')
    else:
        form = ProductForm()

    return render(request, 'admin_product_form.html', {'form': form, 'title': 'Add New Creation'})


@user_passes_test(admin_check)
def admin_product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('custom_admin')
    else:
        form = ProductForm(instance=product)

    return render(request, 'admin_product_form.html', {'form': form, 'title': 'Edit Creation'})


@user_passes_test(admin_check)
def admin_product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product removed from the collection.")
        return redirect('custom_admin')
    return redirect('custom_admin')
