from django.contrib import admin
from .models import *
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fields = (
        "title",
        "author",
        "public",
        "created_at"
    )

class TippaniAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Tippani)
