from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductDetail, PorductSpecifications, ProductStock


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']
        
class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = ['stock_quantity', 'is_available']
        
        
class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PorductSpecifications
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    product_image_front = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name','category', 'price', 'product_image_front']
        
class ProductDetailsSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True, read_only=True)
    product_stock = ProductStockSerializer(many=True, read_only=True)
    product_specification = ProductSpecificationSerializer(many=True, read_only=True)
    product = ProductSerializer()
    class Meta:
        model=ProductDetail
        fields = ['product', 'description', 'product_image', 'product_stock', 'product_specification']
        
