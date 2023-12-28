# your_app/context_processors.py

from ecommerceapp.models import CartItem

def cart_items_count(request):
    if request.user.is_authenticated:
        count = CartItem.objects.filter(cart__user=request.user).count()
    else:
        count = 0
    return {'cart_items_count': count}
