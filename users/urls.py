from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentListAPIView, UserProfileAPIView, PaymentCourseCreateAPIView

app_name = UsersConfig.name

# Описание маршрутизации для ViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('payment_list/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/course/<int:pk>/', PaymentCourseCreateAPIView.as_view(), name='course_payment_create'),
    path('user_detail/<int:pk>/', UserProfileAPIView.as_view(), name='user_detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
