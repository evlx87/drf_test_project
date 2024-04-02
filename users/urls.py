from users.apps import UsersConfig
from users.views import UserViewSet
from rest_framework.routers import DefaultRouter


app_name = UsersConfig.name

# Описание маршрутизации для ViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
urlpatterns = [

] + router.urls