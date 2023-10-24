import django_filters
from blogs.models import Post

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')  # Case-insensitive substring match
    author__username = django_filters.CharFilter(lookup_expr='exact')  # Exact match for author's username

    class Meta:
        model = Post
        fields = ['slug', 'author__username', 'uuid']  # List the fields to be filtered