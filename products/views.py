from django.shortcuts import render
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from .models import (
    Category, 
    Product,
    ProductImage,
    ProductStock, 
    ProductDetail
)
from .serializers import (
    ProductSerializer, 
    ProductStockSerializer,
    ProductDetailsSerializer
)
# Create your views here.

""" 
    =========================
        products View
    =========================
"""
class ProductView(APIView):
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    # def post(self, request, product_id):
    #     # product_id = request.data.get('product_id')
    #     try:
    #         product_details = ProductDetail.objects.get(product = product_id)
    #         serializer = ProductDetailsSerializer(product_details)
    #     except ProductDetail.DoesNotExist:
    #         return Response({"response":"Product details doesn't exist"})
    #     return Response(serializer.data)

@api_view(['GET'])
def ProductDetailsView(request, product_id):
    try:
        product_details = ProductDetail.objects.get(product=product_id)
    except ProductDetail.DoesNotExist:
        return Response({"response":"Product details doesn't exist"})
    serializer = ProductDetailsSerializer(product_details)
    return Response(serializer.data)


""" 
    ======================================
        get products by catagory view
    ======================================
"""
@api_view(['POST'])
def getProductsByCatagory(request):
    
    category = Category.objects.get(slug=request.GET.get('category'))
    products = Product.objects.filter(category=category)
    serializer = ProductSerializer(products, many=True)
    
    return Response(serializer.data)
    
