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

class CategoryTable(admin.ModelAdmin):
    list_display = ['id','name', 'slug', 'created_at']
admin.site.register(Category, CategoryTable)

class ProductTable(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'created_at']
admin.site.register(Product, ProductTable)

class ProductImageTable(admin.ModelAdmin):
    list_display = ['id', 'product', 'product_details', 'image', 'alt_text']
admin.site.register(ProductImage, ProductImageTable)

class ProductSpecificationsTable(admin.ModelAdmin):
    list_display = ['id', 'product', 'specification_name', 'specification_value']
admin.site.register(PorductSpecifications, ProductSpecificationsTable)

class ProductDetailsTable(admin.ModelAdmin):
    list_display = ['id','product', 'description']
admin.site.register(ProductDetail, ProductDetailsTable)

class ProductStockTable(admin.ModelAdmin):
    list_display = ['id', 'category', 'product_details', 'stock_quantity', 'is_available', 'updated_at']
admin.site.register(ProductStock, ProductStockTable)
