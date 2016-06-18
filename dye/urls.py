from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
admin.autodiscover()

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dye.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls',
                           namespace='blog',
                           app_name='blog')),
    url(r'^account/', include('account.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'social-auth/',
        include('social.apps.django_app.urls', namespace='social')),
)
