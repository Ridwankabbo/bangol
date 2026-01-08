from django.shortcuts import render
from rest_framework.decorators import api_view,APIView, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    VerifyOtpSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
# Create your views here.

""" 
    ============================
        Registration View 
    ============================
"""
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def RegistrationView(request):
    if request.method == "POST":
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
""" 
    ============================
        Verify otp view
    ============================
"""
@api_view(["POST"])
@authentication_classes([])
def VerifyOtpView(request):
    if request.method == 'POST':
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            otp = serializer.validated_data.get('otp')
            print(email, otp)
            try:
                user = User.objects.get(email = email)
                if user.otp == otp:
                    user.is_active = True
                    user.otp = None
                    user.save()
                    
                    return Response({"message":"opt verified successfull"})
                    
                return Response({"message":"Invlid otp"})
            except user.DoesNotExist:
                return Response({"message":"User doesn't exist"})
                
        return Response(serializer.errors)
        
""" 
    ===========================
        Forgot password view
    ===========================
"""
from .utils import generate_otp
@api_view(['POST'])
@authentication_classes([])
def forgotPasswordView(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get(email=email)
            
            print(user)
            
            new_verification_otp = generate_otp()
            user.otp = new_verification_otp
            user.save()
            print("new otp: ", user.otp)
            return Response({"message":"new otp code send successfully"})
        except user.DoesNotExist:
            return Response({"message":"User doesn't exist"})
    return Response(serializer.errors)

"""
    ==============================
        Reset password view
    ==============================
"""
@api_view(["POST"])
@authentication_classes([])
def ResetPasswordView(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        otp = serializer.validated_data.get('otp')
        password = serializer.validated_data.get('password')
        
        try:
            user = User.objects.get(email=email)
            if user.otp == otp:
                user.set_password(password)
                user.otp = None
                user.save()
                
                return Response({"message":"password reset successfull"})  
            
            return Response({"message":"Invalid otp"})
        except user.DoesNotExist:
            return Response({"message":"Invalid email/user"})
    return Response(serializer.errors)         
        


