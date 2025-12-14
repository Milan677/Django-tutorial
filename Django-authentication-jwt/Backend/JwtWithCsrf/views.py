from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .authentication import CookieJWTAuthentication
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect




# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    View to set CSRF cookie
    """
    return Response(
        {"message": "CSRF cookie set"},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([AllowAny])
@csrf_protect
def login_view(request):
    """
    Login user and set JWT access & refresh tokens in HttpOnly cookies
    """
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(request, email=email, password=password)

    if user is None:
        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    refresh = RefreshToken.for_user(user)

    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    response = Response(
        {
            "message": "Login successful",
            "user_id": user.id,
        },
        status=status.HTTP_200_OK,
    )

    # -----------------------------
    # Set ACCESS token cookie
    # -----------------------------
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,          # True in production (HTTPS)
        samesite="Lax",       # or "Strict" / "None"
        max_age=60 * 15,      # 15 minutes
    )

    # -----------------------------
    # Set REFRESH token cookie
    # -----------------------------
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )

    return response


@api_view(["POST"])
@authentication_classes([CookieJWTAuthentication])  
@permission_classes([IsAuthenticated])
@csrf_protect
def logout_view(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass

    response = Response(
        {"message": "Logout successful"},
        status=status.HTTP_200_OK,
    )

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return response

