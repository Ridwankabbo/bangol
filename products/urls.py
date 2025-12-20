from django.urls import path
from . import views
urlpatterns = [
    path('', views.ProductView, name='products'),
    path('catagory/<slug:slug>/', views.getProductsByCatagory, name='category.porduct'),

]
