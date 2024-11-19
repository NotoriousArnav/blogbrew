import uuid
from django.db import models
from django.utils.text import slugify
from django.utils.html import strip_tags
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatewords
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    uuid = models.UUIDField(
        default = uuid.uuid4,
        null = False,
        primary_key = True,
    )
    title = models.CharField(
        max_length = 512
    )
    # meta_title = models.CharField(
    #     max_length = 512,
    #     default = '',
    #     null = True,
    # )
    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    content = RichTextField()

    slug = models.SlugField(unique=True, max_length=512, editable=False)
    public = models.BooleanField(default=True)

    # Add a timestamp for publication date
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.slug)])

    def generate_meta_title(self):
        return f"{self.title} - {self.author.username}'s Blog"

    def generate_meta_description(self, max_words=30):
        content_text = strip_tags(self.content)
        truncated_content = truncatewords(content_text, max_words)
        return f"{truncated_content} - Read more on {self.author.username}'s Blog"

    def save(self, *args, **kwargs):
        # Automatically generate the slug from the title
        slug_plus = str(str(self.uuid).split('-')[-1])
        self.slug = slugify(self.title + '-' + slug_plus)
        
        # Automatically generate the meta_title from the title
        self.meta_title = f"{self.title} - Bromine"  # Replace 'Your Blog Name' with your actual blog name

        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.author.username} (Public: {self.public})"


class Tippani(models.Model):
    """Comment Model"""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        # null=True,
        # primary_key=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented {self.text} on {self.post} by {self.post.author}"
