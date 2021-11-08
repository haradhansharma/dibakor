from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily' 

    def items(self):
        return ['feed:feed', 'feed:department-detail', 'feed:search','feed:pc-detail','feed:parser-detail','feed:information']

    def location(self, item):
        return reverse(item)