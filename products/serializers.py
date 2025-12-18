from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductStock

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = "__all__"