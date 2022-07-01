import os
import glob
import json
import jsonpickle
import time
import requests
import vibertelebot.utils.additional_keyboard as addkb
import threading
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
from multiprocessing import Process
from datetime import date, datetime, timedelta
from vibertelebot.textskeyboards import viberkeyboards as kb
from vibertelebot.utils.tools import keyboard_consctructor
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.contact_message import ContactMessage
from viberbot.api.messages.location_message import LocationMessage
from viberbot.api.messages.rich_media_message import RichMediaMessage
from viberbot.api.messages.picture_message import PictureMessage
from viberbot.api.messages.video_message import VideoMessage
from db_func import database as db
from loguru import logger
from db_func import database as db
from sitniks.sender import send_message_viber


dotenv_path = os.path.join(Path(__file__).parent.parent, 'config/.env')
load_dotenv(dotenv_path)


logger.add(
    "logs/info.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="100 MB",
    compression="zip",
)


@logger.catch
def user_message_handler(viber, viber_request):
    """Receiving a message from user and sending replies."""
    logger.info(viber_request)
    # send_message_viber(viber_request)
    message = viber_request.message
    tracking_data = message.tracking_data
    chat_id = viber_request.sender.id
    # Data for usual TextMessage
    reply_text = ''
    reply_keyboard = {}
    # Data for RichMediaMessage
    reply_alt_text = ''
    reply_rich_media = {}
    tracking_data = json.loads(tracking_data)
    tracking_data['QUESTION'] = ''
    if isinstance(message, ContactMessage):
        # Handling reply after user shared his contact infromation
        if message.contact.name:
            tracking_data['NAME'] = message.contact.name
        tracking_data['PHONE'] = message.contact.phone_number
        db.add_user(message.contact.phone_number,
                    chat_id)
        if tracking_data['STATUS'] == 'yes':
            tracking_data = json.dumps(tracking_data)
            reply_text = 'Акаунт знайдено, раді зустрічі знову.'
            reply = [TextMessage(text=reply_text,
                                 tracking_data=tracking_data,
                                 min_api_version=6)]
            viber.send_messages(chat_id, reply)
        else:
            tracking_data = json.dumps(tracking_data)
            reply_text = 'Зареєстрували ✔️'
            reply = [TextMessage(text=reply_text,
                                 tracking_data=tracking_data,
                                 min_api_version=6)]
            viber.send_messages(chat_id, reply)
        time.sleep(0.5)
        reply_text = "Хто Ваш улюбленець?"
        reply_keyboard = kb.pet_keyboard
        tracking_data = json.loads(tracking_data)
        tracking_data['QUESTION'] = reply_text
        tracking_data = json.dumps(tracking_data)
        logger.info(tracking_data)
        reply = [TextMessage(text=reply_text,
                             keyboard=reply_keyboard,
                             tracking_data=tracking_data,
                             min_api_version=6)]
        viber.send_messages(chat_id, reply)
    else:
        text = viber_request.message.text
        logger.info(text)
        if type(tracking_data) is str:
            tracking_data = json.loads(tracking_data)
        if tracking_data['CHAT'] != 'yes':
            if text == 'yes':
                reply_text = "Для підтвердження Вашого акаунту вкажіть, будь ласка, номер телефону або поділіться контактом."
                reply_keyboard = addkb.SHARE_PHONE_KEYBOARD
                tracking_data['STATUS'] = 'yes'
            elif text == 'no':
                reply_text = "Раді знайомству, вкажіть будь ласка, номер телефону або поділіться контактом для створення вашого акаунту."
                reply_keyboard = addkb.SHARE_PHONE_KEYBOARD
                tracking_data['STATUS'] = 'no'
            elif text[:3] == 'pet':
                reply_text = "Супер, чим можем бути корисні?"
                reply_keyboard = kb.menu_keyboard
                db.add_task(chat_id)
            elif text == 'order':
                reply_text = "Дякуємо за звернення, менеджер вже приєднується до чату. Що саме бажаєте замовити?"
                reply_keyboard = kb.menu_keyboard
                tracking_data['CHAT'] = 'yes'
                db.delete_task(chat_id)
            elif text == 'question':
                reply_text = "Дякуємо за звернення, менеджер вже приєднується до чату. Напишіть, будь-ласка, питання."
                reply_keyboard = kb.menu_keyboard
                tracking_data['CHAT'] = 'yes'
                db.delete_task(chat_id)
            elif text == 'consult':
                reply_text = "Дякуємо за звернення, поки менеджер приєднується до чату напишіть, будь-ласка, для кого бажаєте підібрати корм?"
                reply_keyboard = kb.menu_keyboard
                tracking_data['CHAT'] = 'yes'
                db.delete_task(chat_id)
            elif text == 'website':
                reply_text = "Дякуємо за звернення, вітаємо у сімʼїбренду здорового та корисного харчування practik.ua"
                reply_keyboard = kb.menu_keyboard
            elif text == 'back':
                reply_text = "Хто Ваш улюбленець?"
                reply_keyboard = kb.pet_keyboard
            else:
                reply_text = "Дякуємо за звернення, менеджер вже приєднується до чату. Напишіть, будь-ласка, питання."
                reply_keyboard = kb.menu_keyboard
                tracking_data['CHAT'] = 'yes'
                db.delete_task(chat_id)
            tracking_data['QUESTION'] = reply_text
            logger.info(tracking_data)
            if reply_text:
                tracking_data = json.dumps(tracking_data)
                reply = [TextMessage(text=reply_text,
                                     keyboard=reply_keyboard,
                                     tracking_data=tracking_data,
                                     min_api_version=6)]
                viber.send_messages(chat_id, reply)
