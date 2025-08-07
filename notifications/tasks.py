from celery import shared_task
from notification_service import settings
from .models import Notification, DeliveryAttempt
from .utils.email_sender import send_email
from .utils.sms_sender import send_sms
from .utils.telegram_sender import send_telegram


@shared_task
def send_notification(notification_id):
    notification = Notification.objects.get(id=notification_id)
    user = notification.user

    # Select enabled channels
    channels = [
        name for name, enabled in [
            ('email', settings.SMTP_ENABLED),
            ('sms', settings.SMS_ENABLED),
            ('telegram', settings.TELEGRAM_ENABLED),
        ] if enabled
    ]

    for channel in channels:
        # Attempt to send notification via each channel
        success = False
        error = ""
        try:
            if channel == 'email' and user.email:
                success = send_email(user.email, notification.title, notification.message)
            elif channel == 'sms' and user.phone_number:
                success = send_sms(user.phone_number, notification.message)
            elif channel == 'telegram' and user.telegram_id:
                success = send_telegram(user.telegram_id, notification.message)
        except Exception as e:
            error = str(e)

        # Save delivery attempt
        DeliveryAttempt.objects.create(
            notification=notification,
            channel=channel,
            success=bool(success),
            error_message=error if not success else None
        )

        if success:
            notification.is_sent = True
            notification.save()
            # Stop if one channel succeeded
            break