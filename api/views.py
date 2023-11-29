from django.shortcuts import render
from rest_framework import generics, response, views, status, permissions
from django.contrib.auth.models import User
from socialapps_rest_login.models import UserProfile
from .serializers import *
from .filters import PostFilter
import django_filters.rest_framework
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the post.
        return obj.author == request.user

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

    permission_classes = [IsAuthorOrReadOnly]

    def get(self, request, slug):
        # Retrieve the blog post by slug, or return a 404 response if it doesn't exist
        blog_post = get_object_or_404(Post, slug=slug)

        # Serialize the blog post data
        serializer = PostSerializer(blog_post)

        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        # Retrieve the blog post by slug, or return a 404 response if it doesn't exist
        blog_post = get_object_or_404(Post, slug=slug)

        if blog_post.author != request.user:
            return response.Response({'detail': 'You do not have permission to update this post.'}, status=status.HTTP_403_FORBIDDEN)


        # Serialize the updated data and save it
        serializer = PostSerializer(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        # Retrieve the blog post by slug, or return a 404 response if it doesn't exist
        blog_post = get_object_or_404(Post, slug=slug)
        

        if blog_post.author != request.user:
            return response.Response({'detail': 'You do not have permission to update this post.'}, status=status.HTTP_403_FORBIDDEN)

        # Delete the blog post
        blog_post.delete()
        
        return response.Response(status=status.HTTP_204_NO_CONTENT)

class CreateBlogPostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Customize the behavior when creating a new blog post
        serializer.save(author=self.request.user)

from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated

class CommentListView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        comments = Tippani.objects.filter(post=post)
        serializer = TippaniSerializer(comments, many=True)
        return response.Response(serializer.data)

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        data = {
            "user": request.user.id,  # Automatically set the user
            "post": post.uuid,           # Automatically set the post
            "text": request.data.get('text')
        }
        serializer = TippaniSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, slug, uuid):
        post = get_object_or_404(Post, slug=slug)
        comment = get_object_or_404(Tippani, uuid=uuid, post=post, user=self.request.user)
        # Check if the user is the author of the comment or has permission to delete
        if comment.user == request.user:
            comment.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return response.Response({'detail': 'You do not have permission to delete this comment.'}, status=status.HTTP_403_FORBIDDEN)
