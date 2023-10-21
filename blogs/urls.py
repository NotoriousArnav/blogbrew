from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="landing"),
    path("blogs/", BlogListView.as_view(), name="Blogs"),
    path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/<slug:slug>/edit/', BlogUpdateView.as_view(), name='blog-edit'),
    path('blogs/<slug:slug>/comment/', CommentCreateView.as_view(), name="comment-new"),
    path('blogs/<slug:slug>/comment/edit/', CommentUpdateView.as_view(), name="comment-new"),
    path('new/blogs/', BlogCreateView.as_view(), name='blog-create'),
]