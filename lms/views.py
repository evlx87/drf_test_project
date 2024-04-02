from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, ListAPIView, UpdateAPIView, CreateAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscription
from lms.paginators import MaterialsPagination
from lms.permissions import IsModerator, IsOwner
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from lms.tasks import course_update_notification


# Create your views here.
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [~IsModerator]

        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsModerator | IsOwner]

        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsModerator | IsOwner]

        elif self.action in ['destroy']:
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        course_id = self.kwargs.get('pk')
        course = get_object_or_404(Course, id=course_id)

        for field in request.data:
            if hasattr(course, field):
                setattr(course, field, request.data.get(field))

        course.save()

        subscriptions = Subscription.objects.filter(course=course).select_related('user', 'course')
        for subscription in subscriptions:
            course_update_notification.delay(subscription.course.title, subscription.user.email)
        return Response({'message': f'курс "{course}" обновлен'}, status=HTTP_200_OK)


class LessonDetailView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator]
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]


class LessonListView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MaterialsPagination
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]

    def update(self, request, *args, **kwargs):
        lesson = self.get_object()
        serializer = self.get_serializer(lesson, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        lesson.last_updated = timezone.now()
        lesson.save()

        subscriptions = Subscription.objects.filter(course=lesson.course)
        for subscription in subscriptions:
            course_update_notification.delay(lesson.course.title, subscription.user.email)

        return Response({'message': f'урок "{lesson}" обновлен'}, status=HTTP_200_OK)


class LessonCreateView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [~IsModerator]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

        new_lesson = serializer.instance
        subscriptions = Subscription.objects.filter(course=new_lesson.course)
        for subscription in subscriptions:
            course_update_notification.delay(new_lesson.course.title, subscription.user.email)


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course_id = self.kwargs.get('pk')
        course = get_object_or_404(Course, id=course_id)

        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        new_subscription.course = course
        new_subscription.save()


class SubscriptionDestroyAPIView(DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        course_id = self.kwargs.get('pk')
        user_id = self.request.user.pk

        try:
            subscription = Subscription.objects.get(
                course_id=course_id, user_id=user_id)
            if self.request.user != subscription.user:
                message = 'нельзя удалить чужую подписку'
                raise ValidationError(message)
            else:
                self.perform_destroy(subscription)
                return Response({'message': 'подписка удалена'},
                                status=HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'message': 'подписка не найдена'},
                            status=HTTP_404_NOT_FOUND)


class SubscriptionListAPIView(ListAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    pagination_class = MaterialsPagination
    permission_classes = [IsAuthenticated]
