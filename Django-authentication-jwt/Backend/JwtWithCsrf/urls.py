from django.urls import path
from .views import *


urlpatterns = [
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('login/',login_view, name='login'),
    path('logout/',logout_view, name='logout'),
]