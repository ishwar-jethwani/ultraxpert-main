from django.contrib import sitemaps
from django.urls import reverse
from django.contrib.sites.models import Site

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'hourly'

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='ultraxpert.com', name='ultraxpert.com')
        return super(StaticViewSitemap, self).get_urls(site=site, **kwargs)

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