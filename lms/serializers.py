from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson
from lms.validators import YoutubeUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            YoutubeUrlValidator(field='url_video'),
            serializers.UniqueTogetherValidator(
                queryset=Lesson.objects.all(),
                fields=('title', 'description'),
            ),
        ]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = '__all__'
