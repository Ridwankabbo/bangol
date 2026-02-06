from django.urls import path
from . import views
urlpatterns = [
    path('checkout/', views.CheckoutAPIView, name='checkout'),
]
