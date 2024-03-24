from django.contrib import admin

from users.models import User, Payment


# Register your models here.
@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('email', 'phone', 'avatar', 'city', 'role', )


@admin.register(Payment)
class AdminPayment(admin.ModelAdmin):
    list_display = ('user', 'payment_date', 'course', 'lesson', 'amount',)
