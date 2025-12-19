from django.shortcuts import render
from rest_framework.decorators import APIView, api_view
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

""" 
    =========================
        All products View
    =========================
"""
@api_view(['GET'])
def ProductView(request):
    
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
        
    return Response(serializer.data)

""" 
    ======================================
        get products by catagory view
    ======================================
"""
@api_view(['GET'])
def getProductsByCatagory(request, slug):
    
    category = Category.objects.get(name=slug)
    products = Product.objects.filter(category=category)
    serializer = ProductSerializer(products, many=True)
    
    return Response(serializer.data)
    
