from django import forms
from .models import CartItem, Order, Item

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'payment_status', 'service_type', 'mode_of_service']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price'] 


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['date_paid', 'date_collected']  # Only include the fields we want to update

    # Customize the form fields
    date_paid = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    date_collected = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
