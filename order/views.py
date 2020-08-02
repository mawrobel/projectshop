from django.shortcuts import render
from .models import OrderItem
from .forms import OrderForm
from cart.cart import Cart
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import permissions

@permission_classes((permissions.AllowAny,))
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
        else:
            form = OrderForm()
            context = {
                'cart': cart,
                'form': form,
            }
            return render(request, 'orders/order/create.html', context)


@permission_classes((permissions.AllowAny,))
class order_create_api(APIView):

    def get(self, request):
        cart = Cart(request)
        form = OrderForm()
        context = {
            'cart': cart,
            'form': form,
        }
        return render(request, 'orders/order/create.html', context)

    def post(self, request):
        cart = Cart(request)
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
