from django.urls import path
from . import views
urlpatterns = [
    path('', views.CartView, name='cart-view'),
    path('add/', views.AddToCartAuthenticated, name='add'),
    path('delete/', views.DeleteCartItemView, name='delete'),
    path('update/',views.UpdateCartItemView, name='update'),
    path('add-guest-cart/', views.AddToCartGuest, name='Add-gust-cart')
]
