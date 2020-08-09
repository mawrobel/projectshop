from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from io import BytesIO
import weasyprint
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from order.models import Order


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        order = get_object_or_404(Order, id=ipn_obj.invoice)
        order.paid = True
        order.save()
        subject = 'ProjectShop - Receipt nr {}'.format(order.id)
        message = "in this email we are sending the bill "
        email = EmailMessage(subject,
                             message,
                             'admin@projectshop.com',
                             [order.email])
        context = {
            'order': order,
        }
        html = render_to_string('orders/order/pdf.html', context)
        out = BytesIO
        stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
        email.attach('order nr {}.pdf'.format(order.id),
                     out.getvalue(),
                     'application/pdf')
        email.send()


valid_ipn_received.connect(payment_notification)
