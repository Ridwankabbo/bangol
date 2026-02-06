from django.shortcuts import render
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem
from cart.models import Cart, CartItem

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CheckoutAPIView(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    
    if not cart:
        return Response({"response":"Cart is empty"})
    
    with transaction.atomic():
        total = sum(cart_item.quantity * cart_item.product.price for cart_item in cart.cart_item.all())
        
        order = Order.objects.create(
            user=user,
            total_amount=total
        )
        for cart_item in cart.cart_item.all():
            OrderItem.objects.create(
                order = order,
                product = cart_item.product,
                quantity = cart_item.quantity,
                price_at_purchase = cart_item.product.price
            )
        
        cart.cart_item.all().delete()
        
    return Response({
        "responce":"Order placed successfull",
        "order_id":order.id,
        "total": str(total)
    })
        
            
    


