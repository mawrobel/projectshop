from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    image = serializers.ImageField()
    slug = serializers.SlugField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    available = serializers.BooleanField()

    class Meta:
        model = Product
        fields = ('name', 'image', 'slug', 'price' 'available')
