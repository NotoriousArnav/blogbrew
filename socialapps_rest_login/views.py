from django.shortcuts import render
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.github import views as github_views
from django.urls import reverse
from dj_rest_auth.registration.views import SocialLoginView
# Create your views here.

class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    #callback_url = "/accounts/github/login/callback"
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return self.request.build_absolute_uri(reverse('github_callback'))
