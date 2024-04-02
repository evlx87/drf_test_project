from django.contrib import admin

from lms.models import Course, Lesson


# Register your models here.
@admin.register(Course)
class AdminCourse(admin.ModelAdmin):
    list_display = ('name', 'preview', 'description', 'owner',)


@admin.register(Lesson)
class AdminLesson(admin.ModelAdmin):
    list_display = ('course', 'name', 'description', 'preview', 'video_url', 'owner',)
