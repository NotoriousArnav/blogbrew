from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<str:username>/', Profile.as_view(), name="profile_view"),
    path('edit-profile/', UserProfileUpdateView.as_view(), name='edit_profile'),
    path('avatar/<str:username>', ProfilePicture.as_view(), name="avatar"),
]