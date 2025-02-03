# inventory/models.py
from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from datetime import timedelta
import random
from django.db import transaction
import logging

logger = logging.getLogger('inventory')

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - NGN {self.price}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def total_price(self):
        """
        Calculate the total price of all items in the cart by summing the total_price of each CartItem.
        """
        total = 0
        for cart_item in self.cartitem_set.all():  # Iterate over all related CartItems
            total += cart_item.total_price()  # Add the total price of each CartItem
        return total



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        """
        Calculate the total price of this CartItem (price * quantity).

        """
        return self.item.price * self.quantity
    

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=15)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('not_paid', 'Not Paid')], default='not_paid')
    service_type = models.CharField(max_length=10, choices=[('standard', 'Standard'), ('premium', 'Premium')], default='standard')
    mode_of_service = models.CharField(max_length=10, choices=[('delivery', 'Delivery'), ('pickup', 'Pickup'), ('branch', 'Branch')], default='delivery')
    collection_date = models.DateTimeField(null=True, blank=True)
    date_paid = models.DateTimeField(null=True, blank=True)
    date_collected = models.DateTimeField(null=True, blank=True)

    def total_price(self):
        """
        Calculate the total price of the order by summing the total_price of each CartItem in the cart.
        """
        return sum(item.total_price() for item in self.cart.cartitem_set.all())

    def calculate_collection_date(self):
        """
        Calculate the collection date based on the service type.
        """
        if not self.order_date:  # Ensure order_date is set before proceeding
            raise ValueError("Order date is not set")

        if self.service_type == 'standard':
            # Add 7 days for standard service
            self.collection_date = self.order_date + timedelta(days=7)
        elif self.service_type == 'premium':
            # Add a random time between 24 to 48 hours for premium service
            hours_to_add = random.randint(24, 48)
            self.collection_date = self.order_date + timedelta(hours=hours_to_add)

    def save(self, *args, **kwargs):
        if not self.collection_date:  # If collection_date is not set yet, calculate it
            if not self.order_date:
                self.order_date = timezone.now()  # Fallback in case the order_date was not set correctly
            self.calculate_collection_date()  # Calculate the collection date

        super().save(*args, **kwargs)  # Call the parent save method to save the instance

    def move_to_processed(self):
        """
        Move the order to the processed orders list only if date_paid and date_collected are set.
        """
        if self.date_paid and self.date_collected:
            with transaction.atomic():
                processed_order = ProcessedOrder.objects.create(
                    order=self,
                    customer_name=self.customer_name,
                    customer_phone=self.customer_phone,
                    order_date=self.order_date,
                    payment_status=self.payment_status,
                    service_type=self.service_type,
                    mode_of_service=self.mode_of_service,
                    collection_date=self.collection_date,
                    date_paid=self.date_paid,  # Include date_paid in ProcessedOrder
                    date_collected=self.date_collected,  # Include date_collected in ProcessedOrder
                    total_price=self.total_price()
                )

            return processed_order 
          
                
        else:
            raise ValueError("Order must be paid and collected before it can be moved.")


class ProcessedOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=15)
    order_date = models.DateTimeField()
    payment_status = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('not_paid', 'Not Paid')])
    service_type = models.CharField(max_length=10, choices=[('standard', 'Standard'), ('premium', 'Premium')])
    mode_of_service = models.CharField(max_length=10, choices=[('delivery', 'Delivery'), ('pickup', 'Pickup'), ('branch', 'Branch')])
    collection_date = models.DateTimeField(null=True, blank=True)
    date_paid = models.DateTimeField(null=True, blank=True)
    date_collected = models.DateTimeField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Processed Order {self.id} - {self.customer_name}"
    