from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="landing"),
    path("blogs/", BlogListView.as_view(), name="Blogs"),
    path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail')
]