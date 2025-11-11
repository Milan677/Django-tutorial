from django.urls import path
from .views import user_profile, GoogleLogin

urlpatterns = [
    path('google/', GoogleLogin.as_view(), name='google_login'),  # REST social login
    path('profile/', user_profile),  # protected profile
  
]