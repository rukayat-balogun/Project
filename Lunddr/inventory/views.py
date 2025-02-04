# inventory/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Item, Cart, CartItem, Order, ProcessedOrder
from .forms import OrderForm, ItemForm, CartItemForm, OrderUpdateForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
import uuid
from django.core.paginator import Paginator
from django.conf import settings
import requests
import phonenumbers
import pandas as pd
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect('product_listing')  # Redirect to the home page or product listing
            else:
                messages.error(request, 'Invalid username or password.')

        else:
            messages.error(request, 'Invalid form submission.')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('product_listing')

def home(request):
    cart_id = request.session.get('cart_id')
    print(f"Cart ID from session: {cart_id}")
    
    if not cart_id:
        print("No cart_id found in session.")  # Debugging

        # Clear any existing cart session before starting a new order
        if 'cart_id' in request.session:
            del request.session['cart_id']  # Clear the existing cart session

        if request.user.is_authenticated:
            # If the user is logged in, create a cart linked to the user
            new_cart = Cart.objects.create(user=request.user)
        else:
            # If the user is not logged in, create an anonymous cart (without user)
            new_cart = Cart.objects.create()

        request.session['cart_id'] = new_cart.id  # Set the new cart ID in the session
        print(f"Cart ID from session after login: {new_cart.id}")

    return render(request, 'home.html')


def clear_cart_and_home(request):
    # Clear the cart session
    if 'cart_id' in request.session:
        del request.session['cart_id']  # Remove the cart from the session
    
    # Optionally create a new empty cart for the user (if using a session-based cart)
    new_cart = Cart.objects.create(user=request.user)  # Assuming user is logged in; adapt as needed
    request.session['cart_id'] = new_cart.id  # Assign the new cart_id to the session

    # Redirect to the product listing page for a fresh new order
    return redirect('product_listing')  # Redirect to home (product listing)


def product_listing(request):
    # Fetch all items (products)
    products = Item.objects.all()
    return render(request, 'product_listing.html', {'products': products})


def add_product(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new product
            return redirect('product_listing')  # Redirect to the product listing page after adding the product
    else:
        form = ItemForm()

    return render(request, 'add_product.html', {'form': form})


def add_to_cart(request, item_id):
    # Get the item to be added to the cart
    item = Item.objects.get(id=item_id)

    # Get the quantity from the POST request (default to 1 if not provided)
    quantity = int(request.POST.get('quantity', 1))

    # Calculate the total price based on quantity and item price
    total_price = item.price * quantity

    # Check if the user has a cart session or create a new one
    cart_id = request.session.get('cart_id')
    if not cart_id:
        # Create a new cart if no cart exists
        cart = Cart.objects.create(user=request.user if request.user.is_authenticated else None)
        request.session['cart_id'] = cart.id  # Store the cart ID in the session
    else:
        # If the cart already exists, retrieve it
        cart = Cart.objects.get(id=cart_id)

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    if not created:
        # If the item is already in the cart, update the quantity and total price
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f"Quantity of {item.name} updated to {cart_item.quantity}.")
    else:
        # If it's a new item in the cart, set the quantity and total price
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"{item.name} has been added to your cart with quantity {cart_item.quantity}.")

    # Redirect the user back to the product listing page or the current page
    return redirect('product_listing') 



def view_cart(request):
    cart_id = request.session.get('cart_id')
    
    if cart_id:
        cart = Cart.objects.get(id=cart_id)  # Retrieve the cart
        total_price = cart.total_price()  # Calculate the total price using the method
        cart_items = cart.cartitem_set.all()  # Fetch all CartItem objects
    else:
        cart = None
        cart_items = []
        total_price = 0

    return render(request, 'view_cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price
    })


def update_quantity(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            return redirect('view_cart')

    else:
        form = CartItemForm(instance=cart_item)

    return render(request, 'update_quantity.html', {
        'form': form,
        'cart_item': cart_item
    })

@login_required
def checkout(request):
    cart_id = request.session.get('cart_id')
    print(f"Cart ID from session: {cart_id}")  # Debugging

    if not cart_id:
        messages.error(request, "No cart found. Please add items to your cart before checking out.")
        return redirect('product_listing')

    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        messages.error(request, "Cart not found.")
        return redirect('product_listing')

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            # Create the order, linking it to the cart
            order = form.save(commit=False)
            order.cart = cart  # Link the order to the current cart
            order.save()

            print(f"Order created with ID: {order.id}")  # Debugging

            # Optionally, save the order id in the session to maintain context for the user
            request.session['order_id'] = order.id

            # Remove the cart session after order submission (optional)
            del request.session['cart_id']

            # Redirect to order confirmation
            return redirect('order_confirmation')  # Ensure the correct redirect

        else:
            print(f"Form errors: {form.errors}")
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form, 'cart': cart})



def place_order(request):
    # Get cart information
    cart_id = request.session.get('cart_id')
    if not cart_id:
        messages.error(request, "No cart found. Please add items to your cart first.")
        return redirect('product_listing')

    cart = Cart.objects.get(id=cart_id)
    
    # Get order details (assumed to be passed via POST request)
    customer_name = request.POST.get('customer_name')
    customer_phone = request.POST.get('customer_phone')
    service_type = request.POST.get('service_type')

    # Create the order and set the order date automatically
    order = Order.objects.create(
        cart=cart,
        customer_name=customer_name,
        customer_phone=customer_phone,
        service_type=service_type,
    )

    # Save the order (this will also call the overridden save method, calculating the collection date)
    order.save()  # This ensures collection_date is set

    messages.success(request, f"Your order has been placed. Collection date: {order.collection_date}")
    
    return redirect('order_confirmation', order_id=order.id)



def order_confirmation(request):
    order_id = request.session.get('order_id')
    if not order_id:
        messages.error(request, "No order found. Please complete your checkout.")
        return redirect('product_listing')

    try:
        order = Order.objects.get(id=order_id)
        cart = order.cart  # Retrieve cart from the order
        cart_items = cart.cartitem_set.all()  # Get all the items in the cart
    except Order.DoesNotExist:
        messages.error(request, "No order found for this session.")
        return redirect('checkout')

    total_price = sum(cart_item.total_price() for cart_item in cart_items)

    # Send SMS notification with order details
    send_order_confirmation_sms(
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        order_id=order.id,
        total_price=total_price,
        collection_date=order.collection_date.strftime('%b %d, %Y %H:%M'),
        cart_items=cart_items  # Pass cart items to the SMS function
    )

    return render(request, 'order_confirmation.html', {
        'order': order,
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_id': cart.id,
        'order_id': order.id,
        'collection_date': order.collection_date,  # Ensure collection_date is passed to the template
    })



def send_order_confirmation_sms(customer_name, customer_phone, order_id, total_price, collection_date, cart_items):
    try:
        # Parse the phone number for Nigeria (using "NG" for Nigeria)
        phone_number = phonenumbers.parse(customer_phone, "NG")  # "NG" for Nigeria
        formatted_phone_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValueError(f"Invalid phone number format: {customer_phone}")
    
    items_list = "\n".join([f"{item.item.name} (Qty: {item.quantity})" for item in cart_items])
    

    # Prepare the SMS message body
    message_body = f"""
    Hello {customer_name},
    
    Your order (ID: {order_id}) has been confirmed. Here are the details:
    Ordered Items:
    {items_list}
    
    Total Price: NGN {total_price}
    Collection Date: {collection_date}
    
    Thank you for your order!
    """

    # Prepare the BulkSMS API request data
    data = {
        'api_token': settings.BULKSMS_API_KEY,  # Your BulkSMS API key from settings
        'from': 'Lunddr',  # Replace with your desired sender name or number (max 11 characters)
        'to': formatted_phone_number,  # The phone number in E.164 format
        'body': message_body,  # The message body
        'gateway': 'direct-refund',  # Optionally specify the gateway type (default is 'direct-refund')
        'append_sender': 'hosted',  # Optionally specify how the sender ID should be appended
        'callback_url': 'https://yourcallbackurl.com',  # Optional: Add callback URL if needed
        'customer_reference': str(order_id),  # Optional: Unique reference for this SMS
    }

    # Send the POST request to BulkSMS API
    url = "https://www.bulksmsnigeria.com/api/v2/sms"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        if response_data['data']['status'] == 'success':
            print(f"Message sent successfully to {formatted_phone_number}")
            return response_data  # Return response if needed
        else:
            print(f"Error from BulkSMS: {response_data.get('data', {}).get('message', 'Unknown error')}")
            return None
    else:
        print(f"HTTP Error: {response.status_code}")
        return None    
# views.py
@login_required
def update_order(request, order_id):
    # Fetch the order
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)

        if form.is_valid():
            updated_order = form.save()

            # Ensure that move_to_processed is called if date_paid and date_collected are set
            if updated_order.date_paid and updated_order.date_collected:
                updated_order.move_to_processed()  # Move the order to processed orders
                messages.success(request, "Order has been moved to processed orders.")
                return redirect('processed_orders')  # Redirect to processed orders page
            else:
                messages.success(request, "Order has been updated successfully.")
                return redirect('order_summary', order_id=order.id)  # Stay on the order summary page
        else:
            messages.error(request, "There was an error with the form.")
    else:
        form = OrderUpdateForm(instance=order)

    return render(request, 'update_order.html', {'form': form, 'order': order})



@login_required
def all_orders(request):
    orders = Order.objects.all().order_by('-order_date')  # List orders in descending order of order_date
    return render(request, 'all_orders.html', {'orders': orders})

@login_required
def current(request):
    # Get the search query from GET parameters
    search_query = request.GET.get('search', '')

    # Filter orders by customer name if a search query is provided
    if search_query:
        orders = Order.objects.filter(customer_name__icontains=search_query).order_by('-id')
    else:
        orders = Order.objects.all().order_by('-id')

    # Paginate the orders (10 orders per page)
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the template with the paginated orders
    return render(request, 'current.html', {'page_obj': page_obj})

@login_required
def order_summary(request, order_id):
    # Fetch the order or return 404 if it does not exist
    
    order = get_object_or_404(Order, id=order_id)

  
    if request.method == 'POST':
        # If the form is submitted, attempt to update the order
        form = OrderUpdateForm(request.POST, instance=order)
        
        if form.is_valid():
            # Save the updated order
            updated_order = form.save()

           # If both date_paid and date_collected are set, move the order to processed
            if updated_order.date_paid and updated_order.date_collected:
                try:
                    updated_order.move_to_processed()  # Move the order to processed orders
                    messages.success(request, f"Order {updated_order.id} has been successfully moved to processed orders.")
                    print("Sucessful")
                    return redirect('processed_orders')  # Redirect to processed orders page
                
                except ValueError as e:
                    # If there's an error (e.g., missing data), show the error message
                    messages.error(request, str(e))
                   
                    return redirect('order_summary', order_id=updated_order.id)  # Stay on the order summary page
            else:
                messages.success(request, "Order has been updated successfully.")
                return redirect('order_summary', order_id=updated_order.id)  # Stay on the same page if not moved to processed
        else:
            # If form is invalid, show error messages
            messages.error(request, "There was an error with the form.")
    else:
        # If not POST, just display the form with the current order data
        form = OrderUpdateForm(instance=order)

    # Return the order summary page
    return render(request, 'order_summary.html', {'form': form, 'order': order})



@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            updated_order = form.save()

            # Check if both date_paid and date_collected are set
            if updated_order.date_paid and updated_order.date_collected:
                updated_order.move_to_processed()  # Move the order to processed orders
                messages.success(request, "Order has been moved to processed orders.")
                return redirect('processed_orders')  # Redirect to processed orders page
            else:
                messages.success(request, "Order has been updated successfully.")
                return redirect('order_summary', order_id=updated_order.id)  # Stay on the order summary page
        else:
            messages.error(request, "There was an error with the form.")
    else:
        form = OrderUpdateForm(instance=order)

    return render(request, 'update_order.html', {'form': form, 'order': order})



@login_required
def processed_orders(request):
    # Get the search query from GET parameters
    search_query = request.GET.get('search', '')

    # Filter processed orders by customer name if a search query is provided
    if search_query:
        processed_orders = ProcessedOrder.objects.filter(customer_name__icontains=search_query).order_by('-id')
    else:
        processed_orders = ProcessedOrder.objects.all().order_by('-id')

    # Paginate the processed orders (10 orders per page)
    paginator = Paginator(processed_orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the template with the paginated processed orders
    return render(request, 'processed_orders.html', {'page_obj': page_obj})



@user_passes_test(lambda user: user.is_superuser)
def delete_order(request, order_id):
    # Get the order or return 404 if not found
    order = get_object_or_404(Order, id=order_id)

    # Try to delete the order
    try:
        order.delete()
        messages.success(request, "Order deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting order: {e}")

    # Redirect back to the current orders page
    return redirect('current')



# Export Current Orders to Excel
@login_required
def export_current_orders(request):
    # Get current orders
    orders = Order.objects.all().values('id', 'customer_name', 'order_date', 'payment_status', 'service_type', 'mode_of_service', 'total_price')
    
    # Create a DataFrame
    df = pd.DataFrame(orders)

    # Create an HTTP response with the content type for an Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Current_Orders.xlsx'

    # Write the DataFrame to the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Current Orders')

    return response

# Export Processed Orders to Excel
@login_required
def export_processed_orders(request):
    # Get processed orders
    processed_orders = ProcessedOrder.objects.all().values('id', 'customer_name', 'order_date', 'payment_status', 'service_type', 'mode_of_service', 'total_price', 'collection_date', 'date_paid', 'date_collected')
    
    # Create a DataFrame
    df = pd.DataFrame(processed_orders)

    # Create an HTTP response with the content type for an Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Processed_Orders.xlsx'

    # Write the DataFrame to the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Processed Orders')

    return response
