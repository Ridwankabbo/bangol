from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductStock


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']
        
class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = ['stock_quantity', 'is_available']
        
class ProductSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True, read_only=True)
    product_stock = ProductStockSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['name','category', 'price', 'product_image', 'product_stock', 'created_at']
        
