from django.db import models
from user.models import User
from products.models import Product
from django.utils.crypto import get_random_string
# Create your models here.


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PND','Pending'
        PAID = 'PAID', 'Paid'
        CANCLED = 'CND', 'Cancled'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    order_number = models.CharField(unique=True, editable=False)
    status = models.TextField(choices=OrderStatus.choices, default=OrderStatus.PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number =   f"ORD-{get_random_string(10).upper()}"
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.order_number} - {self.user} created_at: {self.created_at}"       
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True,blank=True)
    price_at_purchase = models.DecimalField(max_digits=12, decimal_places=2) 
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_subtotal(self):
        return self.quantity * self.price_at_purchase
    
    def __str__(self):
        return f"Id: {self.id} product: {self.product.name} reguler price:{self.product.price} price at purches:{self.price_at_purchase}"
    