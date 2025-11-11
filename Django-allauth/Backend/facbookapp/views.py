import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model

User = get_user_model()


class FacebookLoginView(APIView):
    def post(self, request):
        access_token = request.data.get("access_token")
        if not access_token:
            return Response(
                {"error": "Access token required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify token with Facebook Graph API
        fb_url = f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"
        fb_response = requests.get(fb_url)
        data = fb_response.json()

        # Handle invalid or expired token
        if "error" in data:
            return Response(
                {"error": "Invalid or expired Facebook token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract user info
        email = data.get("email")
        full_name = data.get("name")
        fb_id = data.get("id")

        print("==================== user data from facebook ==================")
        print(email)
        print(full_name)
        print(fb_id)

        if not email:
            return Response(
                {"error": "Facebook account has no email permission"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create or get the user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"full_name": full_name}
        )

        # Optionally store fb_id (if you plan to add that field later)
        if hasattr(user, "fb_id"):
            user.fb_id = fb_id
            user.save(update_fields=["fb_id"])

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        print("======= user data ==========")
        user_dict = model_to_dict(user)
        print("======= user data ==========")
        print(user_dict)
        

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "email": user.email,
                "full_name": user.full_name,
            },
            status=status.HTTP_200_OK,
        )
