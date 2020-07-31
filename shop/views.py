from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, api_view
from rest_framework.renderers import TemplateHTMLRenderer
from django.core import serializers
from .serializers import ProductSerializer
import json
from rest_framework.parsers import JSONParser
from .models import Category, ParentChild, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt


@permission_classes((permissions.AllowAny,))
class welcomepage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/shop.html'

    def get(self, request):
        root = get_object_or_404(Category, slug="mainpage")
        children = ParentChild.objects.filter(parent=root)
        context = {
            "categories": children,
        }
        return Response(context)


@permission_classes((permissions.AllowAny,))
class Categorypage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/category.html'

    def get(self, request, category_slug):
        parent = get_object_or_404(Category, slug=category_slug)
        ancestor = get_object_or_404(ParentChild, child=parent)
        subcat = ParentChild.objects.filter(parent=parent)
        query = Product.objects.filter(category=parent)
        #query = ProductSerializer(query, many=True)
        paginator = Paginator(query, 5)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context = {
            "categories": subcat,
            "products": products,
            "parent": parent,
            "ancestor": ancestor
        }
        return Response(context)


@permission_classes((permissions.AllowAny,))
class Productpage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/product.html'

    def get(self, request, category_slug, product_slug):
        product = get_object_or_404(Product, slug=product_slug)

        context = {
            "product": product,
        }
        return Response(context)
