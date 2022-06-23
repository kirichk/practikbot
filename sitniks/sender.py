import os
from pathlib import Path
import requests
from dotenv import load_dotenv
from loguru import logger


dotenv_path = os.path.join(Path(__file__).parent.parent, 'config/.env')
load_dotenv(dotenv_path)
TELEGRAM_BOT_ID = os.getenv("TELEGRAM_BOT_ID")
# TELEGRAM_URL = os.getenv("JIVO_TELEGRAM_WEBHOOK_URL")
# VIBER_URL = os.getenv("JIVO_VIBER_WEBHOOK_URL")


# @logger.catch
# def get_token():
#     URL = 'https://api.sitniks.com/api/authorization/token'
#     auth_token = os.getenv("SITNIKS_SECRET")
#     input = {
#         "client_id": "480",
#         "secret": auth_token
#         }
#     hed = {'Authorization': 'Bearer ' + auth_token,
#            'content-type': 'application/json'}
#     x = requests.post(URL,
#                       json=input,
#                       headers=hed)
#     logger.info(x.json())


@logger.catch
def send_message_telegram(data):
    URL = 'https://compound.sitniks.com/webhooks/telegram/<botId>'
    auth_token = os.getenv("SITNIKS_TOKEN")
    hed = {'content-type': 'application/json'}
    input = {
        "company_id": "480",
        "tab_id": "1"
        }
    x = requests.post(URL,
                      body=data,
                      headers=hed)
    logger.info(x.json())


# if __name__ == '__main__':
#     send_message_telegram()
