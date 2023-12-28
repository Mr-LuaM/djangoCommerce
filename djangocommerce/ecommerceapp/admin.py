from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, Category, UserProfile, Order, OrderItem, Review
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render




@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('display_image', 'name', 'description', 'price', 'category', 'stock', 'created_at', 'updated_at')
    list_filter = ('category',)

   
    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />'.format(obj.image.url))

    display_image.short_description = 'Image'
    display_image.allow_tags = True

class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    fields = ['name', 'description', 'price', 'category', 'stock', 'image']
    
    def display_image(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "-"
    display_image.short_description = 'Image'

    def has_change_permission(self, request, obj=None):
       
        return True



@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    inlines = [ProductInline]



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['product', 'quantity']
    readonly_fields = ['product', 'quantity']

    def has_add_permission(self, request, obj=None):
       
        return False

    def has_change_permission(self, request, obj=None):
       
        return False

    def has_delete_permission(self, request, obj=None):
    
        return False
    
    

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('customer', 'total_price', 'order_date', 'status_colored', 'is_delivered')
    actions = ['mark_as_delivered', 'mark_as_not_delivered', 'mark_as_shipped']

    def get_readonly_fields(self, request, obj=None):
        if obj:  
            if obj.status == 'CN': 
                return ['customer', 'total_price', 'order_date', 'billing_details', 'shipping_details', 'notes', 'status_colored', 'is_delivered']
            else:
                return ['customer', 'total_price', 'order_date', 'billing_details', 'shipping_details', 'notes', 'is_delivered']
        return self.readonly_fields

    def has_add_permission(self, request, obj=None):
        # Disallow adding new orders
        return False

    def has_change_permission(self, request, obj=None):
      
        if obj and obj.status != 'CN':  
            return True
        return False

    def status_colored(self, obj):
        colors = {
            'PD': 'blue',  # Pending
            'SH': 'orange',  # Shipped
            'CM': 'green',  # Completed
            'CN': 'red',  # Cancelled
        }
        status_display = obj.get_status_display()
        return format_html('<span style="color: {};">{}</span>', colors.get(obj.status, 'black'), status_display)

    status_colored.short_description = 'Status'
    def mark_as_delivered(self, request, queryset):
        queryset.exclude(status='CN').update(status='CM', is_delivered=True)

    mark_as_delivered.short_description = 'Mark selected orders as delivered'

    def mark_as_not_delivered(self, request, queryset):
        queryset.exclude(status='CN').update(is_delivered=False)

    mark_as_not_delivered.short_description = 'Mark selected orders as not delivered'

    def mark_as_shipped(self, request, queryset):
        queryset.exclude(status='CN').update(status='SH')

    mark_as_shipped.short_description = 'Mark selected orders as shipped'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
   

    def get_queryset(self, request):
        """
        Only show the current user's profile.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  
        elif UserProfile.objects.filter(user=request.user).exists():
            return qs.filter(user=request.user) 
        else:
           
            UserProfile.objects.create(user=request.user)
            return qs.filter(user=request.user)

    def has_add_permission(self, request, obj=None):
        """
        Disallow adding new user profiles for staff users.
        """
        return request.user.is_superuser 

    def has_change_permission(self, request, obj=None):
        """
        Allow changing only if it's the user's own profile or if the user is a superuser.
        """
        if request.user.is_superuser:
            return True  
        if obj is not None:
            return obj.user == request.user
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Allow deletion of profiles only for superusers.
        """
        return request.user.is_superuser
    
@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    pass
