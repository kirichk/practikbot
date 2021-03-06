import os
import time
import ast
import requests
import locale
import json
import jsonpickle
import glob
# import pprint
from pathlib import Path
from dotenv import load_dotenv
from datetime import date, datetime, timedelta
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton)
from telegram.ext import CallbackContext, ConversationHandler
from db_func import database as db
from loguru import logger
from sitniks.sender import send_message_telegram


dotenv_path = os.path.join(Path(__file__).parent.parent, 'config/.env')
load_dotenv(dotenv_path)
# pp = pprint.PrettyPrinter(indent=4)
TOKEN = os.getenv("TOKEN")

logger.add(
    "logs/info.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="100 MB",
    compression="zip",
)

# locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
PET, PHONE, MENU, ANSWER_MENU = range(4)


@logger.catch
def greetings_handler(update: Update, context: CallbackContext):
    # logger.info(update)
    # json_data = str(update)
    # convertedDict = ast.literal_eval(json_data)
    # logger.info(type(convertedDict))
    # logger.info(convertedDict)
    # new_json_data = json.loads(json_acceptable_string)
    # logger.info(new_json_data)
    context.bot.send_message(chat_id=update.message.from_user.id,
                             text="Вітаю у чат-боті українського виробника їжі для собак та котів PRACTIK!")
    time.sleep(0.5)
    user_data = db.check_user(update.message.from_user.id)
    logger.info(user_data)
    if user_data:
        contact_keyboard = [[KeyboardButton("Створити замовлення")],
                            [KeyboardButton("ЄПитання")],
                            [KeyboardButton(
                                "Потрібна консультація експерта з харчування")],
                            [KeyboardButton("Перейти на сайт")],
                            [KeyboardButton("Назад")]]
        reply_markup = ReplyKeyboardMarkup(keyboard=contact_keyboard,
                                           resize_keyboard=True)
        text = "Чим можемо бути корисні?"
        context.bot.send_message(chat_id=update.message.from_user.id,
                                 text=text,
                                 reply_markup=reply_markup)
    else:
        contact_keyboard = [KeyboardButton("Так"),
                            KeyboardButton("Ні"), ]
        reply_markup = ReplyKeyboardMarkup(keyboard=[contact_keyboard],
                                           resize_keyboard=True)
        text = "Ви вже купували PRACTIK раніше?"
        context.bot.send_message(chat_id=update.message.from_user.id,
                                 text=text,
                                 reply_markup=reply_markup)
    context.user_data['QUESTION'] = text
    return PHONE


@logger.catch
def phone_handler(update: Update, context: CallbackContext):
    send_message_telegram(update, context)
    if update.message.text == "Так":
        text = "Для підтвердження Вашого акаунту вкажіть, будь ласка, номер телефону або поділіться контактом."
        context.user_data['Source'] = update.message.text
    elif update.message.text == "Ні":
        text = "Раді знайомству, вкажіть будь ласка, номер телефону або поділіться контактом для створення вашого акаунту."
        context.user_data['Source'] = update.message.text
    else:
        text = "Невірний формат номеру, будь ласка, вкажіть номеру у форматі 0730008023 або поділіться контактом."
    contact_keyboard = [KeyboardButton('Поділитися номером телефону',
                                       request_contact=True,)]
    reply_markup = ReplyKeyboardMarkup(keyboard=[contact_keyboard],
                                       resize_keyboard=True)
    context.bot.send_message(chat_id=update.message.from_user.id,
                             text=text,
                             reply_markup=reply_markup)
    context.user_data['QUESTION'] = text
    return PET


@logger.catch
def pet_handler(update: Update, context: CallbackContext):
    # with open('data.json', 'w', encoding='utf-8') as f:
    #     json_data = ast.literal_eval(str(update))
    #     json.dump(json_data, f, ensure_ascii=False, indent=4)
    send_message_telegram(update, context)
    try:
        phone = update.message.contact.phone_number
    except:
        phone = None
    if not phone:
        if str(update.message.text[0]) == '0' and len(str(update.message.text)) == 10:
            phone = update.message.text
        else:
            phone_handler(update, context)
    if phone:
        context.user_data['PHONE'] = phone
        db.add_user(context.user_data['PHONE'],
                    update.message.from_user.id)
        if context.user_data['Source'] == 'Так':
            text = "Акаунт знайдено, раді зустрічі знову."
            context.bot.send_message(chat_id=update.message.from_user.id,
                                     text=text)
        if context.user_data['Source'] == 'Ні':
            text = "Зареєстрували ✔️"
            context.bot.send_message(chat_id=update.message.from_user.id,
                                     text=text)
        contact_keyboard = [[KeyboardButton("Собака 🐕"),
                             KeyboardButton("Котик 🐈")],
                            [KeyboardButton("Собака та котик 🐾")]]
        reply_markup = ReplyKeyboardMarkup(keyboard=contact_keyboard,
                                           resize_keyboard=True)
        text = "Хто Ваш улюбленець?"
        context.bot.send_message(chat_id=update.message.from_user.id,
                                 text=text,
                                 reply_markup=reply_markup)
        context.user_data['QUESTION'] = text
        return MENU


@logger.catch
def menu_handler(update: Update, context: CallbackContext):
    send_message_telegram(update, context)
    if update.message.text == "/start":
        greetings_handler(update, context)
        return PHONE
    contact_keyboard = [[KeyboardButton("Створити замовлення")],
                        [KeyboardButton("ЄПитання")],
                        [KeyboardButton(
                            "Потрібна консультація експерта з харчування")],
                        [KeyboardButton("Перейти на сайт")],
                        [KeyboardButton("Назад")]]
    reply_markup = ReplyKeyboardMarkup(keyboard=contact_keyboard,
                                       resize_keyboard=True)
    text = "Супер, чим можем бути корисні?"
    context.bot.send_message(chat_id=update.message.from_user.id,
                             text=text,
                             reply_markup=reply_markup)
    db.add_task(update.message.from_user.id)
    context.user_data['QUESTION'] = text
    return ANSWER_MENU


@logger.catch
def menu_answer_handler(update: Update, context: CallbackContext):
    send_message_telegram(update, context)
    db.delete_task(update.message.from_user.id)
    if update.message.text == "Назад":
        contact_keyboard = [[KeyboardButton("Собака 🐕"),
                             KeyboardButton("Котик 🐈")],
                            [KeyboardButton("Собака та котик 🐾")]]
        reply_markup = ReplyKeyboardMarkup(keyboard=contact_keyboard,
                                           resize_keyboard=True)
        text = "Хто Ваш улюбленець?"
        context.bot.send_message(chat_id=update.message.from_user.id,
                                 text=text,
                                 reply_markup=reply_markup)
        context.user_data['QUESTION'] = text
        return MENU
    if update.message.text == "/start":
        greetings_handler(update, context)
        return PHONE
    if update.message.text == "Перейти на сайт":
        inline_keyboard = [InlineKeyboardButton(
            text='Посилання', url='https://practik.ua/')],
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        context.bot.send_message(chat_id=update.message.from_user.id,
                                 text="Дякуємо за звернення, вітаємо у сімʼїбренду здорового та корисного харчування practik.ua")
        return MENU
    if update.message.text == 'Створити замовлення':
        text = "Дякуємо за звернення, менеджер вже приєднується до чату. Що саме бажаєте замовити?"
        context.bot.send_message(chat_id=update.message.from_user.id,
                                 text=text)
        context.user_data['CHAT'] = 'yes'
        context.user_data['QUESTION'] = text
        return ANSWER_MENU
    if update.message.text == 'ЄПитання':
        text = "Дякуємо за звернення, менеджер вже приєднується до чату. Напишіть, будь-ласка, питання."
        context.bot.send_message(chat_id=update.message.from_user.id,
                                 text=text)
        context.user_data['CHAT'] = 'yes'
        context.user_data['QUESTION'] = text
        return ANSWER_MENU
    if update.message.text == 'Потрібна консультація експерта з харчування':
        text = "Дякуємо за звернення, поки менеджер приєднується до чату напишіть, будь-ласка, для кого бажаєте підібрати корм?"
        context.bot.send_message(chat_id=update.message.from_user.id,
                                 text=text)
        context.user_data['CHAT'] = 'yes'
        context.user_data['QUESTION'] = text
        return ANSWER_MENU
    else:
        text = "Дякуємо за звернення! Будь ласка зачекайте, співробітник компанії підключиться до чату в найближчий час."
        if 'CHAT' in context.user_data:
            if context.user_data['CHAT'] != 'yes':
                context.bot.send_message(chat_id=update.message.from_user.id,
                                         text=text)
                context.user_data['QUESTION'] = text
            else:
                context.user_data['QUESTION'] = ''
            context.user_data['CHAT'] = 'yes'
        else:
            context.bot.send_message(chat_id=update.message.from_user.id,
                                     text=text)
            context.user_data['CHAT'] = 'yes'
            context.user_data['QUESTION'] = text
        return ANSWER_MENU
