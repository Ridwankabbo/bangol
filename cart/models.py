from django.db import models
from django.contrib.auth import get_user
from products.models import Product
from user.models import User
# Create your models here.

""" 
    ===================== 
        Cart model
    =====================
"""
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user
    
""" 
    ===================
        CartItem
    ===================
"""
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart: {self.cart} product: {self.product}"