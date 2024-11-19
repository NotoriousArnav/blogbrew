from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy

from .models import Post


class PostFeed(Feed):
    title = "Bromine"
    description = "Latest on Bromine"
    link = reverse_lazy("blogs:posts_list")

    def items(self):
        return Post.published.all()

    def item_title(self, item):
        return item.title
        
    def item_description(self):
        return item.generate_meta_description()
