

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# REST endpoint for Google login
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

# Example protected user profile endpoint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return Response({
        "user_id": user.id,
        "email": user.email,
        "fullname": getattr(user, 'fullname', '')
    })







