from django.urls import path
from . import views
urlpatterns = [
    path('', views.CartView, name='cart-view'),
    path('add/', views.AddToCartAuthenticated, name='add'),
    path('add-gust-cart/', views.AddToCartGuest, name='Add-gust-cart')
]
