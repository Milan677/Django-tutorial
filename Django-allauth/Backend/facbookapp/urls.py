from django.urls import path
from .views import FacebookLoginView

urlpatterns = [
path('facebook/', FacebookLoginView.as_view(), name='facebook-login'),
]