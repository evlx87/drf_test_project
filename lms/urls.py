from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonListView, LessonCreateView, LessonDetailView, LessonUpdateView, \
    LessonDestroyView, SubscriptionListAPIView, SubscriptionCreateAPIView, SubscriptionDestroyAPIView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='courses')


urlpatterns = [
    path('', LessonListView.as_view(), name='lesson_list'),
    path('create/', LessonCreateView.as_view(), name='lesson_create'),
    path('<int:pk>', LessonDetailView.as_view(), name='lesson_detail'),
    path('<int:pk>/update/', LessonUpdateView.as_view(), name='lesson_update'),
    path('<int:pk>/delete/', LessonDestroyView.as_view(), name='lesson_delete'),
    path('subscription/', SubscriptionListAPIView.as_view(), name='subscription_list'),
    path('subscription/create/<int:pk>/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscription/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscription_delete'),
] + router.urls
