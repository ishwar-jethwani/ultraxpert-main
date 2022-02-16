from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'hourly'

    def items(self):
        return ['home',
                'about',
                'banner',
                'contact',
                "blog",
                'category',
                'services',
                'auto_complete',
                'user_plan']

    def location(self, item):
        return reverse(item)