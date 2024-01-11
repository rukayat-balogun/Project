from django.shortcuts import render

# Create your views here.
from django.views import View
from .models import MenuItem, Category, OrderModel

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'laundryapp/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'laundryapp/about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from the category
        native = MenuItem.objects.filter(category__name__contains='Native')
        sport = MenuItem.objects.filter(category__name__contains='Sport')
        casual = MenuItem.objects.filter(category__name__contains='Casual')

        #pass into the context
        context =   {
            'native': native,
            'sport': sport,
            'casual': casual

        }

        #render the templates

        return render(request, 'laundryapp/order.html', context)


    def post(self, request, *args, **kwargs):
        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0

            item_ids = []

            #add the price of all items picked

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
            order = OrderModel.objects.create(price=price)
            order.items.add(*item_ids)


            context = {
                'items': order_items['items'],
                'price': price
                }

            return render(request, 'laundryapp/order_confirmation.html', context)