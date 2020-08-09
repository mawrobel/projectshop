from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('order/', include('order.urls', namespace='orders')),
    path('', include('shop.urls')),
]