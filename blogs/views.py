from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user_agents import parse
import json, random
from django.views.generic import ListView, DetailView
from socialapps_rest_login.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from .models import Post
from .models import Tippani as Comment

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog_form.html'  # Replace with your template name
    fields = ['title', 'content']  # Fields to include in the form
    success_url = '/blogs/'  # Replace with your desired URL after creating a new blog post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog_form.html'  # Replace with your template name
    fields = ['title', 'content']  # Fields to include in the form
    success_url = '/blogs/'  # Replace with your desired URL after editing a blog post

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

# Create your views here.
@csrf_exempt
def index(req):
    # if req.is_mobile:
    #     return render(req, "landing-mobile.html")
    ua = parse(req.META.get('HTTP_USER_AGENT'))
    if ua.is_mobile:
        return render(req, "landing-mobile.html")
    blogs = Post.objects.order_by('-created_at')[:5]
    users = list(sorted(UserProfile.objects.all(), key=lambda x: random.random()))[:10]
    print(users)
    return render(
            req,
            "landing.html",
            context = {
                "blogs": blogs,
                "users": users,
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
        obj = self.get_object()
        m = Post.objects.filter(author=obj.author)
        n = sorted(Post.objects.order_by('-created_at')[:5], key=lambda x: random.random())
        comments = Comment.objects.filter(post=obj)
        context['m'] = m
        context['n'] = n
        context['comments'] = comments
        return context

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    # form_class = CommentForm
    template_name = 'comment_form.html'  # Create this template
    fields = ['text']
    success_url = '/'  # Replace with your desired URL after posting a comment

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(slug=self.kwargs['slug'])
        return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    # form_class = CommentForm
    template_name = 'comment_form.html'  # Create this template
    fields = ['text']
    # success_url = '/'  # Replace with your desired URL after posting a comment

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(slug=self.kwargs['slug'])
        return super().form_valid(form)