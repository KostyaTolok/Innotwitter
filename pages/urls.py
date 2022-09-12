from django.urls import path
from rest_framework import routers
from pages.views import PageViewSet, TagViewSet

app_name = 'pages'

router = routers.SimpleRouter()

router.register(r'pages', PageViewSet, 'pages')
router.register(r'tags', TagViewSet, 'tags')

urlpatterns = router.urls
