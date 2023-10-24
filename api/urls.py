from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
# router.register(r'user/<str:username>/profile/', UserProfileModelViewSet)


urlpatterns = [
    path('user/<str:username>/profile', UserProfileModelViewSet.as_view()),
    path('blogs/', BlogListView.as_view()),
]