from rest_framework import routers
from .views import GeneratorView, SnippetsViewSet

router = routers.DefaultRouter()

router.register(r'generator', GeneratorView, basename='generator')
router.register(r'snippets', SnippetsViewSet, basename='snippets')
router.register(r'snippets/(?P<snippet_name>[\w\d-]+)', SnippetsViewSet, basename='snippet')

urlpatterns = router.urls
