from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from user_agents import parse
import json, random
from django.views.generic import ListView, DetailView
from socialapps_rest_login.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from .models import Post
from .models import Tippani as Comment
import bleach

allowed_tags = ['a', 'p', 'strong', 'em', 'ul', 'ol', 'li'] + list(bleach.sanitizer.ALLOWED_TAGS) + ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'img']
bleach.sanitizer.ALLOWED_ATTRIBUTES.update({
    'img': ['src', 'alt', 'height', 'width'],
    'a': ['href', 'title'],
    'p': [],
    'strong': [],
    'em': [],
    'ul': [],
    'ol': [],
    'li': [],
})

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog_form.html'  # Replace with your template name
    fields = ['title', 'content', 'public']  # Fields to include in the form
    success_url = '/'  # Replace with your desired URL after creating a new blog post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog_form.html'  # Replace with your template name
    fields = ['title', 'content', 'public']  # Fields to include in the form
    success_url = '/'  # Replace with your desired URL after editing a blog post

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

# Create your views here.
@csrf_exempt
def index(req):
    # if req.is_mobile:
    #     return render(req, "landing-mobile.html")
    if req.user.is_authenticated:
        return redirect(
                    reverse(
                            "Blogs"
                        )
                )
    ua = parse(req.META.get('HTTP_USER_AGENT'))
    blogs = Post.objects.filter(public=True).order_by('-created_at')[:5]
    users = list(
                sorted(
                    UserProfile.objects.exclude(pfp="av.jpg"),
                    key=lambda x: random.random()
                )
            )[:10]
    if ua.is_mobile:
        return render(
                    req,
                    "landing-mobile.html",
                    context = {
                            "blogs": blogs,
                            "users": users,
                        }
                )
    return render(
            req,
            "landing.html",
            context = {
                "blogs": blogs,
                "users": users, #[::-1],
            }
        )

class BlogListView(ListView):
    model = Post
    template_name = 'blog_list.html'  # Replace with the actual template name
    context_object_name = 'blog_posts'
    ordering = ['-created_at']  # Optional: to order the posts by creation date

    def get_queryset(self):
        # Filter only public blog posts
        return Post.objects.filter(public=True).order_by('-created_at')

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
        sanitized_content = bleach.clean(
                obj.content,
                attributes=bleach.sanitizer.ALLOWED_ATTRIBUTES,
                tags=allowed_tags
            )

        m = sorted(
                    Post.objects.filter(author=obj.author, public=True),
                    key=lambda x: random.random()
                )
        n = sorted(
                    Post.objects.filter(public=True).order_by('-created_at')[:5],
                    key=lambda x: random.random()
                )
        comments = Comment.objects.filter(post=obj)
        context['m'] = m
        context['n'] = n
        context['comments'] = comments
        context['sanitized_content'] = sanitized_content
        return context

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    # form_class = CommentForm
    template_name = 'comment_form.html'  # Create this template
    fields = ['text']
    success_url = '../'  # Replace with your desired URL after posting a comment

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(slug=self.kwargs['slug'])
        return super().form_valid(form)

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'
    success_url = '../../../'

    def get_object(self, queryset=None):
        comment = Comment.objects.get(uuid=self.kwargs['uuid'])
        return comment
