from django.urls import path
from .views import *


urlpatterns = [
    # CSRF token
    path('csrf/',get_csrf_token),
    path('check-session-expire-or-not/',check_session),
    
    path('register/', register_user, name='register'),
    path('login/',login_user, name='login'),
    path('logout/',logout_user, name='logout'),
    path('protected/',protected_view, name='protected-view'),
    
]