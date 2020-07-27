from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import CategorySerializer
from .models import Category, ParentChild, Product


@permission_classes((permissions.AllowAny,))
class welcomepage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/shop.html'

    def get(self, request):
        children = ParentChild.objects.filter(id=1)
        context = {
            "categories": children,
        }
        return Response(context)


@permission_classes((permissions.AllowAny,))
class Categorypage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/category.html'

    def get(self, request, category_slug):
        parent = Category.objects.filter(slug=category_slug)
        subcat = ParentChild.objects.filter(parent=parent[0])
        context = {
            "categories": subcat,
        }
        return Response(context)


@permission_classes((permissions.AllowAny,))
class Productpage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/product.html'

    def get(self, request):
        context = {
        }
        return Response(context)
