from rest_framework import routers
from pages.views import PageViewSet, TagViewSet

router = routers.SimpleRouter()

router.register(r'pages', PageViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = router.urls
