import os
import time
import json
from pathlib import Path
from dotenv import load_dotenv
from db_func.database import (task_list, add_counter, delete_task)
from telegram import Bot
from telegram.utils.request import Request
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup)
from telegram.ext import CallbackContext, ConversationHandler
from vibertelebot.main import viber
from viberbot.api.messages.text_message import TextMessage
from vibertelebot.textskeyboards import viberkeyboards as kb
from loguru import logger


dotenv_path = os.path.join(Path(__file__).parent.parent, 'config/.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv("TOKEN")

bot = Bot(token=os.getenv("TOKEN"))


def send_message_to_user(user_id):
    try:
        int(user_id)
        contact_keyboard = [[KeyboardButton("Створити замовлення")],
                            [KeyboardButton("ЄПитання")],
                            [KeyboardButton(
                                "Потрібна консультація експерта з харчування")],
                            [KeyboardButton("Перейти на сайт")],
                            [KeyboardButton("Назад")]]
        reply_markup = ReplyKeyboardMarkup(keyboard=contact_keyboard,
                                           resize_keyboard=True)
        bot.send_message(chat_id=user_id,
                         text="Вітаємо! Як нам відомо улюбленець сам себе не нагодує) Продовжимо вибір харчування?",
                         reply_markup=reply_markup)
    except:
        viber.send_messages(user_id, [TextMessage(text="Вітаємо! Як нам відомо улюбленець сам себе не нагодує) Продовжимо вибір харчування?",
                                               keyboard=kb.menu_keyboard])


@logger.catch
def task_checker():
    while 1:
        try:
            tasks = task_list()
            logger.info(tasks)
            for item in tasks:
                if int(item[1]) == 1440:
                    send_message_to_user(item[0])
                    delete_task(item[0])
                else:
                    add_counter(item[0], item[1])
        except Exception as e:
            logger.warning(e)
        finally:
            time.sleep(60)
