from django.db import models
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

    
class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    alt_text = models.CharField(max_length=150)
    
    def __str__(self):
        return self.product.name
    
    
class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_details')
    # images = models.ForeignKey(ProductImage, on_delete=models.CASCADE)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.product.name} description: {self.description}"
    
    
    
class PorductSpecifications(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_specification')
    specification_name = models.CharField(max_length=100)
    specification_value = models.CharField(max_length=100)
    
    def __str__(self):
        return self.product.name
    
class ProductStock(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_catagory')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_stock')
    stock_quantity = models.IntegerField()
    is_available = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"catagory:{self.category} product:{self.product} stoke quantity:{self.stock_quantity}"
    
    