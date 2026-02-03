from django.db import models
from user.models import User
from products.models import Product
# Create your models here.


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PND','Pending'
        PAID = 'PAID', 'Paid'
        CANCLED = 'CND', 'Cancled'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    order_number = models.IntegerField(unique=True, editable=False)
    status = models.TextField(choices=OrderStatus.choices, default=OrderStatus.PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True,blank=True)
    price_at_purchase = models.DecimalField(max_digits=12, decimal_places=2) 
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    