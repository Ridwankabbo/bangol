from django.urls import path
from . import views
urlpatterns = [
    path('', views.ProductView.as_view(), name='products'),
    path('<int:product_id>/', views.ProductDetailsView, name='product-details'),
    path('catagory/', views.getProductsByCatagory, name='category.porduct'),

]
