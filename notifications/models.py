from django.core.validators import RegexValidator
from django.db import models


phone_validator = RegexValidator(
    regex=r'^\+7\d{10}$',
    message='Phone number must be in the format +7XXXXXXXXXX (11 digits).'
)


class User(models.Model):
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[phone_validator],
        null=True,
        blank=True
    )
    telegram_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.email or self.phone_number or f"Telegram: {self.telegram_id}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification to {self.user}"


class DeliveryAttempt(models.Model):
    CHANNEL_CHOICES = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('telegram', 'Telegram'),
    )

    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)