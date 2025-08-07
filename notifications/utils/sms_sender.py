import logging
from notification_service import settings
from notifications.utils.external_services.mts_api import MTS_SMS


sms = MTS_SMS(settings.SMS_API_KEY, debug=settings.DEBUG)

def send_sms(phone: str, message: str):
    try:
        response = sms.send_sms(phone, message, sender=settings.SMS_API_SENDER)
        if response:
            logging.info(f"✅ SMS sent to {phone}")
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"❌ Failed to send SMS to {phone}: {e}")
        return False
