from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .models import (
    Category, 
    Product,
    ProductImage,
    ProductStock
)
from .serializers import (
    ProductSerializer, 
    ProductStockSerializer
)
# Create your views here.

class ProductView(APIView):
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        
        return Response(serializer.data)
