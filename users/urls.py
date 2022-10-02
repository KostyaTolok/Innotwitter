from rest_framework.routers import SimpleRouter

from users.views import UserViewSet

app_name = 'users'

router = SimpleRouter()

router.register("users", UserViewSet, 'users')

urlpatterns = router.urls
