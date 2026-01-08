from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from .serializers import CartSerializer
# Create your views here.

@api_view(['GET'])
def CartView(request):
    cart = Cart.objects.filter(user=request.user)
    serializer = CartSerializer(cart, many=True)
        
    return Response(serializer.data)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddToCartAuthenticated(request):
    
    if request.method == 'POST':
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        
        cart, created = Cart.objects.get_or_create(user = request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product_id
        )        
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
            
        cart_item.save()
        return Response({"message":"Item added to cart", "cart_id":cart.id})
    

@api_view(['POST'])
def AddToCartGuest(request):
    cart_id = request.data.get('cart_id')
    product_id = request.data.get('product_id')
    
    if cart_id:
        cart = Cart.objects.get(id=cart_id, user__isnull=True)
    else:
        cart = Cart.objects.create() # new guest cart
        
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_id=product_id
    )
    
    item.quantity = (item.quantity + 1) if not created else 1
    item.save()
    
    return Response({"cart id": cart_id, "quantity": item.quantity})



