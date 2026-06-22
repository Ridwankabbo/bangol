from django.urls import path
from . import views
urlpatterns = [
    path('', views.ProductView.as_view(), name='products'),
    path('categories/', views.CategoryApiView, name='categories'),
    path('<int:product_id>/', views.ProductDetailsView, name='product-details'),
    path('category/<slug:slug>/', views.getProductsByCatagory, name='category.porduct'),

]
