# socialapps_rest_login/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import UserProfile

class UserProfileSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return UserProfile.objects.all()

    def lastmod(self, obj):
        return obj.user.date_joined  # Use the date_joined field as an approximation for last modification
