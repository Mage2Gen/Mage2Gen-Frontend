from django.contrib import admin
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.urls import reverse, path, re_path, include
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
    path("grappelli/", include("grappelli.urls")),
    path("mage_admin/", admin.site.urls),

    path("", include("social_django.urls", namespace="social")),

    path("sitemap.xml", sitemap, {"sitemaps": {"pages": StaticPageSitemaps, "snippets": SnippetSitemaps}},
         name="django.contrib.sitemaps.views.sitemap"),

    path("account/", AccountView.as_view(), name="account"),

    path("", Mage2GenView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("commandline/", CommandlineView.as_view(), name="commandline"),
    path("snippets/", SnippetsView.as_view(), name="snippets"),
    path("snippets/<slug:snippet_name>/", SnippetView.as_view(), name="snippet"),

    path("load/<slug:config_id>/", Mage2GenView.as_view(), name="home_load"),
    path("save/", SaveModuleJsendView.as_view(), name="save"),
    path("save/<slug:config_id>/", SaveModuleJsendView.as_view(), name="resave"),
    re_path(
        r"^download/(?P<download_type>[\w\d-]+)/(?P<config_id>[\w\d-]+)\.(?P<extension>\w+)$",
        DownloadModule.as_view(),
        name="download",
    ),
    path("files/", ModuleFileStructureJsendView.as_view(), name="file_structure"),
    path("files/<slug:config_id>/", ModuleFileStructureJsendView.as_view(), name="file_structure_load"),

    path("api/", include(("apps.mage2gen.api.urls", "apps.mage2gen.api"), namespace="rest_framework")),

    path("user/modules/", UserModulesJsendView.as_view(), name="user_modules"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    except ImportError:
        pass
