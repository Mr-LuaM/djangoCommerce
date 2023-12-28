# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import  SignUpForm,UserProfileForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseForbidden,JsonResponse
from django.db import IntegrityError,transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import UserProfile, Order, OrderItem, Review ,Product, Category, Cart, CartItem
from django.db.models import Count, Avg,Sum,F, ExpressionWrapper, fields

def user_login(request):
    return LoginView.as_view(
        template_name='users/login.html',  
        redirect_authenticated_user=True,
    )(request)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
           
            user = form.save()

          
            UserProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
            )

           
            login(request, user)

            return redirect('/')  
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def index_view(request):
  
    top_products = Product.objects.annotate(purchase_count=Count('orderitem')).order_by('-purchase_count')[:3]

  
    latest_products = Product.objects.order_by('-created_at')[:3]

 
    categories = Category.objects.all()

   
    popular_products_by_category = {}

  
    for category in categories:
    
        if Product.objects.filter(category=category, review__isnull=False).exists():
            popular_products = (
                Product.objects
                .filter(category=category, review__isnull=False)
                .annotate(avg_rating=Avg('review__rating'))
                .order_by('-avg_rating')[:3]
            )
        else:
           
            popular_products = (
                Product.objects
                .filter(category=category)
                .order_by('-created_at')[:3]
            )

        popular_products_by_category[category] = popular_products

    context = {
        'top_products': top_products,
        'latest_products': latest_products,
        'popular_products_by_category': popular_products_by_category,
    }

    return render(request, 'users/index.html', context)
def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    category = product.category 

    context = {
        'product': product,
        'category': category,
    }
    
    
    return render(request, 'users/product_details.html', context)



def product_list(request):
   
    categories = Category.objects.all()
    
    context = {'categories': categories}
    return render(request,'users/products.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        user_profile = request.user.userprofile 

       
        cart, created = Cart.objects.get_or_create(user=user_profile.user)

   
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
        
            cart_item.quantity = quantity
        else:
           
            cart_item.quantity += quantity

        cart_item.save()

        messages.success(request, f"{quantity} {product.name}(s) added to your cart.")

    return redirect('product_details', product_id=product.id)


@login_required
def cart(request):
    cart_items = []
    total_quantity = 0
    total_value = 0

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart__user=request.user)
            
           
            total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum']
            
           
            total_value = cart_items.aggregate(total_value=Sum(F('product__price') * F('quantity')))['total_value'] or 0

        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile not found. Please create a profile.')
            return redirect('/')

    else:
        return redirect('login')

    context = {'cart_items': cart_items, 'total_quantity': total_quantity, 'total_value': total_value}
    return render(request, 'users/cart.html', context)

@login_required
def update_quantity(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 0)

        try:
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=request.user.user_cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()

       

            return JsonResponse({'status': 'success', 'message': 'Quantity updated successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return redirect('cart')  


@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        
        try:
            cart_item = CartItem.objects.get(cart=request.user.user_cart, product_id=product_id)
            cart_item.delete()

            return JsonResponse({'status': 'success', 'message': 'Item removed successfully.'})
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found in cart.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def checkout(request):
    user_profile = UserProfile.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart__user=request.user)

  
    total_price = cart_items.aggregate(total_price=Sum(F('product__price') * F('quantity')))['total_price'] or 0

    context = {
        'user_profile': user_profile,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    if request.method == 'POST':

        billing_details = 'COD'  
        shipping_address = request.POST.get('shipping_address')  
        order_notes = request.POST.get('order_notes')  

       
        with transaction.atomic():
         
            order = Order.objects.create(
                customer=request.user,
                total_price=total_price,
                billing_details=billing_details,
                shipping_details=shipping_address, 
                notes=order_notes,
            )

           
            for cart_item in cart_items:
                OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

               
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()

          
            cart_items.delete()
            
            subject = 'Your Order Details'
            html_message = render_to_string('users/order_email.html', {'order': order, 'user': request.user})
            plain_message = strip_tags(html_message)
            from_email = 'From <alluasan599@gmail.com>'  
            to = request.user.email

            send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return redirect('cart')  

    return render(request, 'users/checkout.html', context)

@login_required
def purchase_history(request):
    user_orders = Order.objects.filter(customer=request.user).order_by('-order_date').prefetch_related('orderitem_set__product')

 
    for order in user_orders:
        for item in order.orderitem_set.all():
            item.total_price = item.product.price * item.quantity

    context = {
        'orders': user_orders,
    }

    return render(request, 'users/purchase_history.html', context)

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user, status=Order.OrderStatus.PENDING)

    if request.method == 'POST':
        order.status = Order.OrderStatus.CANCELLED
        order.save()
        messages.success(request, "Order cancelled successfully.")
        return redirect('order_history')

   
    messages.error(request, "Invalid request.")
    return redirect('purchase_history')

def user_logout(request):
   
    request.session.clear()

   
    logout(request)

  
    return redirect('/') 

@login_required
def edit_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
          
            return redirect('edit_profile')  
    else:
        form = UserProfileForm(instance=profile)

    context = {'form': form}
    return render(request, 'users/edit_profile.html', context)

def categories(request):
   pass
def about(request):
   pass
def contact(request):
   pass


