from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = "Order number {}".format(order_id)
    message = "Welcome {}! You placed an order in our shop. ID of your order is {}. Total cost is $ {} ".format(order.first_name,order.id, order.get_total_cost())
    mail_sent = send_mail(subject,
                          message,
                          'admin@projectshop.com',
                          [order.email])
    return mail_sent
