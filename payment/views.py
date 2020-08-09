from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from paypal.standard.forms import PayPalPaymentsForm
from order.models import Order
from decimal import Decimal


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": '%.2f' % order.get_total_cost(),
        "item_name": 'Order {}.'.format(order.id),
        "invoice": str(order.id),
        "currency_code": 'USD',
        "notify_url": 'http://{}{}'.format(host, reverse('paypal-ipn')),
        "return_url": 'http://{}{}'.format(host, reverse('payment:done')),
        "canceled_return": 'http://{}{}'.format(host, reverse('payment:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        'order': order,
        'form': form,
    }
    return render(request, 'payment/process.html', context)


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
