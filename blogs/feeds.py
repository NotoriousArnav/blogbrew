from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy

from .models import Post


class PostFeed(Feed):
    title = "Bromine"
    description = "Latest on Bromine"
    link = "feeds/"

    def items(self):
        return Post.objects.all()[::-1]

    def item_title(self, item):
        return item.title
        
    def item_description(self, item):
        return item.generate_meta_description()