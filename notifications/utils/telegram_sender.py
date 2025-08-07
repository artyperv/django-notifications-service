import requests
import logging

from notification_service import settings

def send_telegram(tg_id, message):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': tg_id,
        'text': message
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logging.info(f"✅ Telegram message sent to {tg_id}")
            return True
        else:
            logging.error(f"❌ Failed to send Telegram message: {response.text}")
            return False
    except Exception as e:
        logging.error(f"❌ Exception sending Telegram message: {e}")
        return False
