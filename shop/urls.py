from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "ProjectShop"

urlpatterns = [
    path("", views.welcomepage.as_view(), name='main'),

]
urlpatterns += staticfiles_urlpatterns()

