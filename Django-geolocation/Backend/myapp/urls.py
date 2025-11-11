from django.urls import path
from .views import nearest_depot, nearest_three_depot

urlpatterns = [
    path('nearest-depot/', nearest_depot),
    path('nearest-three-depot/', nearest_three_depot),
]
