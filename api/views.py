from django.shortcuts import render
from rest_framework import generics, response, views, status
from django.contrib.auth.models import User
from socialapps_rest_login.models import UserProfile
from .serializers import *
from .filters import PostFilter
import django_filters.rest_framework
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class UserProfileModelViewSet(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
    # Your logic to retrieve and return the user's profile
        user = User.objects.get(username=self.kwargs.get('username'))
        profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(profile)
        user_data = UserSerializer(user)
        posts = Post.objects.filter(author=user)
        blog_data = [PostSerializer(post).data for post in posts]
        dt = serializer.data
        dt['user'] = user_data.data
        dt['posts'] = {
            'posts': blog_data
        }
        return response.Response(dt)

class BlogListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['uuid', 'author__username', 'slug', 'title', 'created_at', 'content']

class PostView(views.APIView):
    def get(self, request, slug):
        # Retrieve the blog post by slug, or return a 404 response if it doesn't exist
        blog_post = get_object_or_404(Post, slug=slug)

        # Serialize the blog post data
        serializer = PostSerializer(blog_post)

        return response.Response(serializer.data, status=status.HTTP_200_OK)

class CreateBlogPostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Customize the behavior when creating a new blog post
        serializer.save(author=self.request.user)