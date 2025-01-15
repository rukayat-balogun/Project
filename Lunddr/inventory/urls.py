# inventory/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Add this line for login
    path('register/', views.register, name='register'),  # Add this line for registration
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),  # Home page URL
    path('add-product/', views.add_product, name='add_product'),
    path('product-listing/', views.product_listing, name='product_listing'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('update-quantity/<int:cart_item_id>/', views.update_quantity, name='update_quantity'),
    path('checkout/', views.checkout, name='checkout'),  # Checkout page
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),  # Order confirmation page
    path('all-orders/', views.all_orders, name='all_orders'),
    path('update-order/<int:order_id>/', views.update_order, name='update_order'),
    
]