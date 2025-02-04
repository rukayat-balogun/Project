import pandas as pd
from django.http import HttpResponse
from django.contrib import admin
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from django.contrib import messages
from .models import Order, Cart, ProcessedOrder, Item
from openpyxl.utils.dataframe import dataframe_to_rows
import pytz
from django.db.models import F, Sum



# Admin action to export current orders as Excel
def export_current_orders(modeladmin, request, queryset):
    # Get current orders data
    orders = queryset.values('id', 'customer_name', 'order_date', 'payment_status', 'service_type', 'mode_of_service', 'total_price')

    # Convert timezone-aware datetime fields to timezone-unaware
    for order in orders:
        # Convert datetime fields to timezone-unaware
        if order['order_date']:
            order['order_date'] = order['order_date'].astimezone(pytz.UTC).replace(tzinfo=None)
        if order['collection_date']:
            order['collection_date'] = order['collection_date'].astimezone(pytz.UTC).replace(tzinfo=None)
        if order['date_paid']:
            order['date_paid'] = order['date_paid'].astimezone(pytz.UTC).replace(tzinfo=None)
        if order['date_collected']:
            order['date_collected'] = order['date_collected'].astimezone(pytz.UTC).replace(tzinfo=None)

    # Create DataFrame
    df = pd.DataFrame(orders)

    # Prepare Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Current_Orders.xlsx'

    # Write to Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Current Orders')

    return response

export_current_orders.short_description = "Export Selected Current Orders as Excel"


# Admin action to export processed orders as Excel
def export_processed_orders(modeladmin, request, queryset):
    # Get processed orders data
    processed_orders = queryset.values('id', 'customer_name', 'order_date', 'payment_status', 'service_type', 'mode_of_service', 'total_price', 'collection_date', 'date_paid', 'date_collected')

    # Convert timezone-aware datetime fields to timezone-unaware
    for order in processed_orders:
        # Convert datetime fields to timezone-unaware
        if order['order_date']:
            order['order_date'] = order['order_date'].astimezone(pytz.UTC).replace(tzinfo=None)
        if order['collection_date']:
            order['collection_date'] = order['collection_date'].astimezone(pytz.UTC).replace(tzinfo=None)
        if order['date_paid']:
            order['date_paid'] = order['date_paid'].astimezone(pytz.UTC).replace(tzinfo=None)
        if order['date_collected']:
            order['date_collected'] = order['date_collected'].astimezone(pytz.UTC).replace(tzinfo=None)

    # Create DataFrame
    df = pd.DataFrame(processed_orders)

    # Prepare Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Processed_Orders.xlsx'

    # Write to Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Processed Orders')

    return response

export_processed_orders.short_description = "Export Selected Processed Orders as Excel"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'order_date', 'payment_status', 'total_price',  'service_type', 'collection_date')
    list_filter = ('service_type', 'collection_date')
    actions = [export_current_orders]  # Adding the export action
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
    actions = [export_processed_orders]  

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total Price'

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # Display name and price in the list view
    search_fields = ('name',)  # Allow search by product name
    list_filter = ('price',)  # Filter products by price

# Admin action to export current orders as Excel




# Register models with the admin interface
# Register the model with the custom admin class
admin.site.register(Item, ItemAdmin)