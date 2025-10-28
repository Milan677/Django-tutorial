from django.urls import path
from .views import nearest_depot

urlpatterns = [
    path('nearest-depot/', nearest_depot),
]
