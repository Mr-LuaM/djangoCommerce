# yourapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def calculate_total_price(cart_items):
    return sum(item.product.price * item.quantity for item in cart_items)
