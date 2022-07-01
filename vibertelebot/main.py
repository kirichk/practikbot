import os
import logging
import json
import time
import requests
from vibertelebot.utils import additional_keyboard as addkb
from pathlib import Path
from dotenv import load_dotenv
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import (ViberFailedRequest,
                                         ViberConversationStartedRequest,
                                         ViberMessageRequest,
                                         ViberSubscribedRequest)
from loguru import logger
from vibertelebot.handlers import user_message_handler
from vibertelebot.utils.tools import keyboard_consctructor
from vibertelebot.textskeyboards import viberkeyboards as kb
from sitniks.sender import send_message_viber
from db_func import database as db


dotenv_path = os.path.join(Path(__file__).parent.parent, 'config/.env')
load_dotenv(dotenv_path)

viber = Api(BotConfiguration(
    name='PractikBot',
    avatar='https://i.ibb.co/xLkPxm6/Instagram-1-1.png',
    auth_token=os.getenv('VIBER_TOKEN')
))


@logger.catch
def main(request):
    request_data = request.get_data()
    viber_request = viber.parse_request(request.get_data())
    json_data = json.loads(str(request_data.decode('ascii')))
    button_list = kb.button_dict.keys()
    if 'message' in json_data:
        if json_data['message']['text'] in button_list:
            json_data['message']['text'] = kb.button_dict[json_data['message']['text']]
    logger.info(json_data)
    # logger.info(viber_request.message)
    send_message_viber(json_data)
    viber_request = viber.parse_request(request.get_data())
    # Defining type of the request and replying to it
    if isinstance(viber_request, ViberMessageRequest):
        user_message_handler(viber, viber_request)
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.user.id, [
            TextMessage(text="Дякую!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn(
            "client failed receiving message. failure: {viber_request}")
    elif isinstance(viber_request, ViberConversationStartedRequest):
        # First touch, sending to user keyboard with phone sharing button
        tracking_data = {'NAME': 'ViberUser', 'HISTORY': '', 'CHAT': 'no'}
        tracking_data = json.dumps(tracking_data)
        viber.send_messages(viber_request.user.id, [
            TextMessage(
                text="Вітаю у чат-боті українського виробника їжі для собак та котів PRACTIK!",
                tracking_data=tracking_data,
                min_api_version=6)
            ]
        )
        user_data = db.check_user(viber_request.user.id)
        logger.info(user_data)
        if user_data:
            time.sleep(0.5)
            viber.send_messages(viber_request.user.id, [
                TextMessage(
                    text="Чим можемо бути корисні?",
                    keyboard=kb.menu_keyboard,
                    tracking_data=tracking_data,
                    min_api_version=6)
                ]
            )
        else:
            time.sleep(0.5)
            viber.send_messages(viber_request.user.id, [
                TextMessage(
                    text="Ви вже купувала PRACTIK раніше?",
                    keyboard=kb.greeting_keyboard,
                    tracking_data=tracking_data,
                    min_api_version=6)
                ]
            )
