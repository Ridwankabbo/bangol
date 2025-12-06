from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('registration/', views.RegistrationView, name='user_registration'),
    path('verify-otp/', views.VerifyOtpView, name='verify-otp'),
    path('forgot-password/', views.forgotPasswordView, name='forgot-password'),
    path('reset-password/', views.ResetPasswordView, name='reset-password'),
    path('login/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
]
