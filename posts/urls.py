from rest_framework import routers

from posts.views import PostViewSet

app_name = 'posts'

router = routers.SimpleRouter()

router.register('posts', PostViewSet, 'posts')

urlpatterns = router.urls
