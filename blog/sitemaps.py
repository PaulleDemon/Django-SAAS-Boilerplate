# generates sitemaps for SEO

from django.contrib.sitemaps import Sitemap
from django.utils.text import slugify

from .models import Blog


class BlogSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Blog.objects.filter(draft=False)

    def lastmod(self, obj):
        return obj.datetime
    
    def location(self,obj):
        return '/blog/%s' % (obj.slug)
