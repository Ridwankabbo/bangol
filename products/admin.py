from django.contrib import admin
from .models import (
    Category,
    Product, 
    ProductImage,
    PorductSpecifications,
    ProductDetail,
    ProductStock
)
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(PorductSpecifications)
admin.site.register(ProductDetail)
admin.site.register(ProductStock)
