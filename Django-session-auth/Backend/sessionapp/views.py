from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token

@api_view(["GET"])
@permission_classes([AllowAny])
def get_csrf_token(request):
    return Response({"csrfToken":get_token(request)})


# check session view - if session is not expire skip login
@api_view(['GET'])
@permission_classes([AllowAny])
def check_session(request):
    if request.user.is_authenticated:
        return Response({
            "authenticated": True,
            "name": request.user.name,
            "email": request.user.email
        })
    return Response({"authenticated": False})


@api_view(['POST'])
@authentication_classes([SessionAuthentication])
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
@authentication_classes([SessionAuthentication])
@permission_classes([AllowAny])
def login_user(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error":"Username and password are required"},status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request,user)
            return Response({"message":"Login sucessfull"},status=status.HTTP_200_OK)    
        else:
            return Response({"error":"Invalid username or password"},status=status.HTTP_401_UNAUTHORIZED)    


    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR

        )   

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        
       logout(request)
       return Response({"message":"Logout successfull"})

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR

        )    


@api_view(['GET'])
def protected_view(request):
    return Response({"message":f"Hello {request.user.name}, this is a protected view !"})