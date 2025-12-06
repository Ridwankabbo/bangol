from rest_framework import serializers
from .models import User
from .utils import generate_otp

""" ===================== Registration Serializer ====================="""
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields =['email','username', 'password']
        
    def create(self, validate_data):
    
        try:
            user = User.objects.create_user(
                email = validate_data.get('email'),
                username = validate_data.get('username'),
                password = validate_data.get('password')
            )
            verification_otp = generate_otp()
            print("OTP:", verification_otp)
            user.otp = verification_otp
            user.save()
        except AttributeError:
            raise ValueError(
                {"detail":"otp not found"}
            )
            
        print(f"OTP for {user.email}: {user.otp}")

        return user
        
""" ===================== Verify otp Serializer ====================="""
class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    
""" ===================== Login Serializer ====================="""
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
""" ===================== Forgot password Serializer ====================="""
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
""" ===================== Reset password Serializer ====================="""
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    otp = serializers.CharField()
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ='__all__'
        

"""
    ===========================================
        Custom token obtain pair serializer
    ===========================================
"""                
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field='email'
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if not user:
                raise exceptions.AuthenticationFailed("NO active account found with the given credentials")
            if not user.is_active:
                raise exceptions.AuthenticationFailed("Account isn't active")
        else:
            raise exceptions.AuthenticationFailed("must include email and password")
        
        
        return super().validate(attrs)