import weasyprint
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import OrderItem, Order
from .forms import OrderForm
from cart.cart import Cart
from .tasks import order_created
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.decorators import permission_classes
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import permissions


@permission_classes((permissions.AllowAny,))
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            order_created.delay(order.id)
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
            # return render(request, 'orders/order/created.html', locals())
    else:
        form = OrderForm()
        context = {
            'cart': cart,
            'form': form,
        }
        return render(request, 'orders/order/create.html', context)


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'admin/orders/order/detail.html', context)


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    html = render_to_string('orders/order/pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = filename = "order_{}".format(order_id)
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT+'css/pdf.css')])
    return response
