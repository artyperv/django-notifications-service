from django.contrib import admin
from .models import User, Notification, DeliveryAttempt
from .tasks import send_notification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone_number', 'telegram_id')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'is_sent', 'created_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Only send notification on creation
            send_notification.delay(obj.id)  # type: ignore

@admin.register(DeliveryAttempt)
class DeliveryAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'notification', 'channel', 'success', 'timestamp')
