import uuid
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
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

    # Add a timestamp for publication date
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically generate the slug from the title
        self.slug = slugify(self.title)
        
        # Automatically generate the meta_title from the title
        self.meta_title = f"{self.title} - Bromine"  # Replace 'Your Blog Name' with your actual blog name

        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
