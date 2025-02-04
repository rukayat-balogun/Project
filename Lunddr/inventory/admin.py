from django.contrib import admin
from .models import Order, Cart, ProcessedOrder, Item

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

@admin.register(ProcessedOrder)
class ProcessedOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'order_date', 'payment_status', 'total_price','collection_date', 'date_paid', 'date_collected')
    list_filter = ('payment_status', 'date_collected')

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total Price'

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # Display name and price in the list view
    search_fields = ('name',)  # Allow search by product name
    list_filter = ('price',)  # Filter products by price

# Register the model with the custom admin class
admin.site.register(Item, ItemAdmin)