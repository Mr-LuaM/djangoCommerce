from django.urls import path
from .views import user_login,signup,index_view,user_logout,product_details,product_list,add_to_cart,cart,update_quantity,checkout,contact,about,categories,remove_from_cart,purchase_history,cancel_order,edit_profile

urlpatterns = [
    path('login/', user_login, name='login'),
    path('signup/', signup, name='signup'),
    path('', index_view, name='index'),  
    path('logout/', user_logout, name='logout'),

      path('product_details/<int:product_id>/', product_details, name='product_details'),
       path('product_list/', product_list, name='product_list'),
       path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
            path('cart/', cart, name='cart'),
              path('checkout/', checkout, name='checkout'),
              path('update_quantity/', update_quantity, name='update_quantity'),
               path('categories/', categories, name='categories'),
                path('about/', about, name='about'),
                 path('contact/', contact, name='contact'),
                 path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
                 path('purchase-history/', purchase_history, name='purchase_history'),
                  path('cancel-order/<int:order_id>/', cancel_order, name='cancel_order'),
path('edit-profile/', edit_profile, name='edit_profile'),
                 
             
        
        

]
