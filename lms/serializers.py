from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()

    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
