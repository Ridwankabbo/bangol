from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from products.models import Product

from .models import Cart, CartItem
from .serializers import CartSerializer
# Create your views here.


""" 
    =========================
        Get Cart view
    =========================
"""

@api_view(['GET'])
def CartView(request):
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        
    else:
        cart_id = request.data.get('cart_id')
        if not cart_id:
            return Response({"Items":[], "grand_total": 0})
        
        try:
            cart = Cart.objects.get_or_create(id=cart_id, user__isnull=True)
        except (Cart.DoesNotExist, ValueError): 
            return Response({"error":"Cart not found"})
        
    serializer = CartSerializer(cart)
        
    return Response(serializer.data)
    
    
""" 
    ================================
        Add to cart Authenticated
    ================================
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddToCartAuthenticated(request):
    
    if request.method == 'POST':
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        
        cart, created = Cart.objects.get_or_create(user = request.user)
        
        product_instance = get_object_or_404(Product, id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product_instance
        )        
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
            
        cart_item.save()
        return Response({"message":"Item added to cart", "cart_id":cart.id})
    
    
""" 
    =========================
        Delete cart
    =========================
"""
@api_view(['DELETE'])
def DeleteCartItemView(request):
    item_id = request.data.get('item_id')
    
    if request.user.is_authenticated:
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
        
        return Response({"message":"Item removed from cart"})
        
    else:
        cart_id = request.data.get('cart_id') or request.quary_params.get('cart_id')
        item = get_object_or_404(CartItem, id=item_id, cart_id=cart_id)

        item.delete()
        
        return Response({"message": "Item removed from class"})
    
        
""" 
    =========================
        Add to cart guest
    =========================
"""

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



