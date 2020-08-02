from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('order/', include('order.urls', namespace='orders')),
    path('', include('shop.urls')),

]