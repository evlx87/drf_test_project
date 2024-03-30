from rest_framework import serializers

from lms.services import create_course_payment
from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = [
            'email',
            'phone',
            'city',
            'avatar',
            'role',
            'password']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class CreatePaymentSerializer(serializers.ModelSerializer):
    course_payment_url = serializers.SerializerMethodField(read_only=True)

    def get_course_payment_url(self, obj):
        result = create_course_payment(
            course=obj.course.title,
            price=int(obj.course.price * 100))
        return result.url

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
