from rest_framework import routers
from pages.views import PageListViewSet, PageDetailViewSet, TagViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'pages', PageListViewSet)
router.register(r'pages', PageDetailViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = router.urls
