from .models import Cart, CartItem
from rest_framework import serializers

  
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        
class CartSerializer(serializers.ModelSerializer):
    cart_item = CartItemSerializer(many=True ,read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'