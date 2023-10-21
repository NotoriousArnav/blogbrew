from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user_agents import parse
import json
from django.views.generic import ListView, DetailView
from .models import Post
from socialapps_rest_login.models import UserProfile

# Create your views here.
@csrf_exempt
def index(req):
    # if req.is_mobile:
    #     return render(req, "landing-mobile.html")
    ua = parse(req.META.get('HTTP_USER_AGENT'))
    if ua.is_mobile:
        return render(req, "landing-mobile.html")
    blogs = Post.objects.order_by('-created_at')[:5]
    return render(
            req,
            "landing.html",
            context = {
                "blogs": blogs
            }
        )

class BlogListView(ListView):
    model = Post
    template_name = 'blog_list.html'  # Replace with the actual template name
    context_object_name = 'blog_posts'
    ordering = ['-created_at']  # Optional: to order the posts by creation date

    # Optional: Add any additional context data if needed
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        return context

class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog_detail.html'  # Replace with the actual template name
    context_object_name = 'blog_post'
    slug_url_kwarg = 'slug'  # Define the slug URL keyword name

    # Optional: Add any additional context data if needed
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        return context