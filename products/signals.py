from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, ProductDetail, ProductImage, ProductStock, PorductSpecifications

@receiver(post_save, sender=Product)
def create_product_details(sender, instance, created, **kwargs):
    if created:
        product_details = ProductDetail.objects.create(
            product = instance
        )
        ProductImage.objects.create(
            product = instance,
            product_details= product_details
        )
        
        