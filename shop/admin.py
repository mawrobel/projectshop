from django.contrib import admin
from .models import User,Category,ParentChild,Product

admin.site.register(User)
admin.site.register(Category)
admin.site.register(ParentChild)
admin.site.register(Product)