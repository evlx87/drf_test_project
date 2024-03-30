from rest_framework import serializers

from lms.services import create_course_payment
from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class PaymentSerializer(serializers.ModelSerializer):
    course_payment_url = serializers.SerializerMethodField(read_only=True)

    def get_course_payment_url(self, obj):
        if obj.course:
            if obj.course.price:
                stripe_response = create_course_payment(
                    course=obj.course.title,
                    price=int(obj.amount * 100))
                return stripe_response.url
            else:
                return 'У курса нет цены'
        else:
            return None

    class Meta:
        model = Payment
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'phone',
            'city',
            'avatar',
            'payments']
