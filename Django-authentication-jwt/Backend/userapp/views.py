from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.hashers import make_password, check_password



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def register_user(request):
    try:
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully", "user": serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def login_user(request):
    try:
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.filter(email=email).first()
        if not user or not check_password(password,user.password):
            return Response({"error":"Invalid email or password !"},status=status.HTTP_401_UNAUTHORIZED)
        
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
                "message": "Login successful",
                "user":{
                    "email":user.email,
                    "name":user.name,
                },
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),    
            }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "error": str(e),
            "message": "Error occurred in login view"
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def protected_view(request):
   return Response({"msg":"hii"})