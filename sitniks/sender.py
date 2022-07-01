import os
import json
import ast
from pathlib import Path
import requests
from dotenv import load_dotenv
from loguru import logger
from telegram import Update


dotenv_path = os.path.join(Path(__file__).parent.parent, 'config/.env')
load_dotenv(dotenv_path)
TELEGRAM_BOT_ID = os.getenv("TELEGRAM_BOT_ID")
VIBER_BOT_ID = os.getenv("VIBER_BOT_ID")
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
def send_message_telegram(data, context):
    URL = f'https://compound.sitniks.com/2.0/webhooks/telegram/{TELEGRAM_BOT_ID}'
    # auth_token = os.getenv("SITNIKS_TOKEN")
    hed = {'content-type': 'application/json'}
    # input = {
    #     "company_id": "480",
    #     "tab_id": "1"
    #     }
    json_data = ast.literal_eval(str(data))
    if 'QUESTION' in context.user_data:
        if context.user_data['QUESTION']:
            json_data['message']['text'] = f"БОТ: {context.user_data['QUESTION']}\n\n{json_data['message']['text']}"
    logger.info(json_data)
    x = requests.post(URL,
                      json=json_data,
                      headers=hed)
    logger.info(x.text)


@logger.catch
def send_message_viber(data):
    URL = f'https://compound.sitniks.com/2.0/webhooks/viber/{VIBER_BOT_ID}'
    # auth_token = os.getenv("SITNIKS_TOKEN")
    hed = {'content-type': 'application/json'}
    # input = {
    #     "company_id": "480",
    #     "tab_id": "1"
    #     }
    # json_data = json.loads(str(data.decode('ascii')))
    x = requests.post(URL,
                      json=data,
                      headers=hed)
    logger.info(x.text)


# if __name__ == '__main__':
#     send_message_telegram()
