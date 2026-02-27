from langchain_core.tools import tool
from products.models import Product
from order.models import Order, OrderItem
import json
from django.db.models import Q

@tool
def search_products(querry:str):
    
    """
    Search for products in the database. 
    Search for products using fuzzy matching. 
    Handles typos (e.g., 'frout' -> 'fruit') and plurals (e.g., 'mobiles' -> 'mobile') and (synonyms like mobile and phoner are basically same).
    scan the  products and category so the typos, purals and synonyms problem shouldn't happen.
    Use this when the user asks to see items, find products, or searches for a specific category.
    Input should be a search string like 'panjabi' or 'blue shirt'.
    """
    
    #print(querry)
    
    words = querry.split()
    
    product_filter = Q()
    
    for word in words:
        if len(word)< 2: continue
        product_filter &= (
            Q(name__icontains = word) |
            Q(category__name__icontains = word)|
            Q(product_details__description__icontains = word)
        )
    
    products = Product.objects.filter(product_filter).distinct()
    
    results = []
    for p in products:
        first_image = p.product_image.first()
        image_url = first_image.image.url if first_image and first_image.image else None
        
        # Get stock info
        stock = p.product_stock.first()
        stock_qty = stock.stock_quantity if stock else 0
        
        results.append({
            "id": p.id,
            "name": p.name,
            "price": str(p.price),
            "category": p.category.name,
            "image": image_url,
            "in_stock": stock_qty > 0
        })
    return json.dumps(results)

@tool
def create_order_from_chat(user_id:int, product_id:int, quantity:int = 1):
    
    """
    Create a new order for a specific product and user.
    Use this when a user explicitly says they want to buy or order an item.
    Requires the product_id (int) and the user_id (int).
    """
    
    try:
        product = Product.objects.get(id=product_id)
        
        total = product.price * quantity
        order = Order.objects.create(
            user_id=user_id,
            total_amount=total,
            status='PND'
        )
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price_at_purchase=product.price
        )
        
        return f"অর্ডার সফলভাবে তৈরি হয়েছে! আপনার অর্ডার নম্বর: {order.order_number}। পেমেন্ট করতে চেকআউট পেজে যান।"
    except Product.DoesNotExist:
        return "দুঃখিত, এই প্রোডাক্টটি খুঁজে পাওয়া যায়নি।"
    except Exception as e:
        return f"Error: {str(e)}"