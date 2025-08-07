from rest_framework.viewsets import ModelViewSet
from .models import Notification
from .serializers import NotificationSerializer
from .tasks import send_notification # type: ignore
from celery.app.task import Task

send_notification: Task


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        notification = serializer.save()
        send_notification.delay(notification.id)