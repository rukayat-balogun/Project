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
    path('current/', views.current, name='current'),
    path('order-summary/<int:order_id>/', views.order_summary, name='order_summary'),  # View order details and update dates
    path('all-orders/', views.all_orders, name='all_orders'),
    path('update-order/<int:order_id>/', views.update_order, name='update_order'),
    path('processed-orders/', views.processed_orders, name='processed_orders'),
    path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('export-current-orders/', views.export_current_orders, name='export_current_orders'),
    path('export-processed-orders/', views.export_processed_orders, name='export_processed_orders'),

    
]