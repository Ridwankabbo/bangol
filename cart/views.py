from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
# Create your views here.

@api_view(['GET'])
def CartView(request):
    if request.method == 'GET':
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        
        return Response(serializer.data)
