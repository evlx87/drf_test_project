from django.contrib import admin

from lms.models import Course, Lesson, Subscription


# Register your models here.
@admin.register(Course)
class AdminCourse(admin.ModelAdmin):
    list_display = ('name', 'preview', 'description', 'owner',)


@admin.register(Lesson)
class AdminLesson(admin.ModelAdmin):
    list_display = ('course', 'name', 'description', 'preview', 'video_url', 'owner',)


@admin.register(Subscription)
class AdminSubscription(admin.ModelAdmin):
    list_display = ('user', 'course',)
