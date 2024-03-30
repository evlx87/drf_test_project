from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from lms.models import Course
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, UserProfileSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method',)
    ordering_fields = ('payment_date',)


class UserProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def get_object(self):
        user = super().get_object()
        user.payments = user.payment_set.all()
        return user


class PaymentCourseCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course_id = self.kwargs.get('pk')
        course = get_object_or_404(Course, id=course_id)
        user = self.request.user

        if user.payment_set.filter(course=course).exists():
            raise serializers.ValidationError('У вас уже есть оплаченное обучение')
        serializer.save(user=user, course=course, amount=course.price)
