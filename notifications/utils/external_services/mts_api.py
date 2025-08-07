import logging

import requests

logger = logging.getLogger(__name__)

# MTS_SMS class to interact with MTS SMS API
class MTS_SMS:
    BASE_URL = "https://api.exolve.ru/messaging/v1/"

    def __init__(self, api_key: str, debug: bool = False):
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.debug = debug

    def send_sms(
        self,
        phone: str,
        message: str,
        sender: str,
        template_id: int | None = None,
    ):
        _command = "SendSMS"
        payload = {"number": sender, "destination": phone, "text": message}
        if template_id:
            payload["template_resource_id"] = template_id  # type: ignore

        url = self.BASE_URL + _command
        try:
            response = requests.post(url, json=payload, headers=self.headers)
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to make request to SMS Center: {e}")
            return None

        if response.status_code != 200:
            logger.error(
                "While trying to send sms got error: %s : %s",
                response.status_code,
                response.text,
            )
        elif self.debug:
            logger.debug(
                "SMS sent. ID: %s",
                response.json().get("message_id"),
            )

        return response.json() if response.status_code == 200 else None


# Usage Example
# api_key = settings.SMS_API_KEY  # Replace with your actual API key
# sms = MTS_SMS(api_key)
# response = sms.send_sms("+79991234567", "Привет!", "MySender", template_id=123456)
