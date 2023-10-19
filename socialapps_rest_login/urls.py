from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from allauth.socialaccount.providers.github import views as github_views

from .views import *

urlpatterns = [
    path('', include('dj_rest_auth.registration.urls')),
    path('github/', GitHubLogin.as_view()),
    path('github/url/', github_views.oauth2_login)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
