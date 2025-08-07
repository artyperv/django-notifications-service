from rest_framework.viewsets import ModelViewSet
from .models import Notification
from .serializers import NotificationSerializer
from .tasks import send_notification


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        # Create the notification instance
        notification = serializer.save()
        # Run Celery task
        send_notification.delay(notification.id)