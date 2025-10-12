# users/views.py
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def google_login(request):
    token = request.data.get("token")
    if not token:
        return Response({'error': 'Token missing'}, status=status.HTTP_400_BAD_REQUEST)


    try:
        # Verify Google token
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        email = idinfo["email"]
        name = idinfo.get("name", "")
        google_id = idinfo["sub"]

        # Create or get user
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={"name": name, "google_id": google_id}
        )

        # Issue JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "email": email,
            "name": name,
            "user_id": user.id,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })

    except ValueError:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # ✅ Requires valid JWT
def get_user_info(request):
    """
    Return user info for the authenticated user
    """
    user = request.user  

    print("============== user info ==============")
    print(user.id)
    print(user.name)
    print(user.email)
    
    

    return Response({
        "id": user.id,
        "name": getattr(user, "name", ""),
        "email": user.email,
        "google_id": getattr(user, "google_id", None),
    }, status=status.HTTP_200_OK)