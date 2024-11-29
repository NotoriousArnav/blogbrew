from rest_framework import serializers
from socialapps_rest_login.models import UserProfile
from django.contrib.auth.models import User
from blogs.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = [
            'uuid',
            'author_username',
            'title',
            'content',
            'created_at',
            'slug',
            'public'
        ]
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['slug'] = instance.slug
        return data

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'public']

    def to_representation(self, instance):
            data = super().to_representation(instance)
            data['slug'] = instance.slug
            return data

class TippaniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tippani
        fields = '__all__'
