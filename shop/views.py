from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import CategorySerializer
from .models import Category


@permission_classes((permissions.AllowAny,))
class welcomepage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/shop.html'
    query = Category.objects.all()
    def get(self, request):
        context = {
            "categories": self.query,
        }
        return Response(context)
