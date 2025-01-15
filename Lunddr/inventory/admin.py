from django.contrib import admin
from .models import Order, Cart

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'order_date', 'payment_status', 'total_price',  'service_type', 'collection_date')
    list_filter = ('service_type', 'collection_date')
    def total_price(self, obj):
        return obj.total_price()  # Call the total_price method from the Order model
    total_price.short_description = 'Total Price'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price')
    
    def total_price(self, obj):
        return obj.total_price()  # Call the total_price method from the Cart model
    total_price.short_description = 'Total Price'
