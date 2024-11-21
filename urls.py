from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.urls import reverse, path
from mage2gen import Snippet
from django.conf.urls.static import static

from apps.mage2gen.views import (Mage2GenView, ads_txt_view,
    DownloadModule, 
    SaveModuleJsendView, 
    ModuleFileStructureJsendView, 
    UserModulesJsendView, 
    AboutView, 
    SnippetsView, 
    SnippetView,
    CommandlineView)

from apps.account.views import AccountView

class StaticPageSitemaps(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return ['home', 'about', 'commandline', 'snippets']

    def location(self, item):
        return reverse(item)

class SnippetSitemaps(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        snippets = []
        for snippet in Snippet.snippets():
            snippets.append(snippet.name().lower())
        return snippets

    def location(self, item):
        return reverse('snippet', kwargs={'snippet_name': item})

urlpatterns = [
    path("ads.txt", ads_txt_view),
	url(r'^grappelli/', include('grappelli.urls')),
    url(r'^mage_admin/', admin.site.urls),

    url('', include('social_django.urls', namespace='social')),

	# Sitemap
	url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'pages': StaticPageSitemaps, 'snippets': SnippetSitemaps}},
		    name='django.contrib.sitemaps.views.sitemap'),

	# Account page
	url(r'^account/$', AccountView.as_view(), name="account"),

    # cached version
    # url(r'^$', cache_page(60 * 60)(Mage2GenView.as_view()), name='home'),
    # url(r'^about/$', cache_page(60 * 60)(AboutView.as_view()) , name='about'),
    # url(r'^commandline/$', cache_page(60 * 60)(CommandlineView.as_view()), name='commandline'),
    # url(r'^snippets/$', cache_page(60 * 60)(SnippetsView.as_view()), name='snippets'),
    # url(r'^snippets/(?P<snippet_name>[\w-]+)/$', cache_page(60 * 60)(SnippetView.as_view()) , name='snippet'),

    url(r'^$', Mage2GenView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view() , name='about'),
    url(r'^commandline/$', CommandlineView.as_view(), name='commandline'),
    url(r'^snippets/$', SnippetsView.as_view(), name='snippets'),
    url(r'^snippets/(?P<snippet_name>[\w-]+)/$', SnippetView.as_view() , name='snippet'),

    url(r'^load/(?P<config_id>[\w\d-]+)/$', Mage2GenView.as_view(), name='home_load'),
    url(r'^save/$', SaveModuleJsendView.as_view(), name='save'),
    url(r'^save/(?P<config_id>[\w\d-]+)/$', SaveModuleJsendView.as_view(), name='resave'),
    url(r'^download/(?P<download_type>[\w\d-]+)/(?P<config_id>[\w\d-]+)\.(?P<extension>\w+)', DownloadModule.as_view(), name='download'),
    url(r'^files/$', ModuleFileStructureJsendView.as_view(), name='file_structure'),
    url(r'^files/(?P<config_id>[\w\d-]+)/$', ModuleFileStructureJsendView.as_view(), name='file_structure_load'),

    # API
    url(r'^api/', include(('apps.mage2gen.api.urls','apps.mage2gen.api'), namespace='rest_framework')),

    url(r'^user/modules/$', UserModulesJsendView.as_view(), name='file_structure'),
]

#Makes media files work on dev server
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
