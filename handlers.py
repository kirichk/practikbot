import os
import time
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


dotenv_path = os.path.join(Path(__file__).parent.parent, 'config/.env')
load_dotenv(dotenv_path)
# pp = pprint.PrettyPrinter(indent=4)
TOKEN = os.getenv("TOKEN")

# locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
PET, PHONE, MENU, ANSWER_MENU = range(4)


def greetings_handler(update: Update, context: CallbackContext):
    contact_keyboard = [KeyboardButton("Так"),
                        KeyboardButton("Ні"), ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[contact_keyboard],
                                       resize_keyboard=True)
    context.bot.send_message(chat_id=update.message.from_user.id,
                             text="Ви вже купувала PRACTIK раніше?",
                             reply_markup=reply_markup)
    return PHONE


def phone_handler(update: Update, context: CallbackContext):
    if update.message.text == "Так":
        text = "Для підтвердження Вашого аккаунту вкажіть, будь ласка, номер телефону або поділіться контактом."
        context.user_data['Source'] = update.message.text
    elif update.message.text == "Ні":
        text = "Раді знайомству, вкажіть будь ласка, номер телефону або поділіться контактом для створення вашого аккаунту."
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
    return PET


def pet_handler(update: Update, context: CallbackContext):
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
        if context.user_data['Source'] == 'Так':
            context.bot.send_message(chat_id=update.message.from_user.id,
                                     text="Аккаунт знайдено, раді зустрічі знову.")
        if context.user_data['Source'] == 'Ні':
            context.bot.send_message(chat_id=update.message.from_user.id,
                                     text="Зареєстрували.")
        contact_keyboard = [[KeyboardButton("Собака"),
                             KeyboardButton("Котик")],
                            [KeyboardButton("Собака та котик")]]
        reply_markup = ReplyKeyboardMarkup(keyboard=contact_keyboard,
                                           resize_keyboard=True)
        context.bot.send_message(chat_id=update.message.from_user.id,
                                 text="Хто Ваш улюбленець?",
                                 reply_markup=reply_markup)
        return MENU


def menu_handler(update: Update, context: CallbackContext):
    contact_keyboard = [[KeyboardButton("Створити замовлення")],
                        [KeyboardButton("ЄПитання")],
                        [KeyboardButton(
                            "Потрібна консультація експерта з харчування")],
                        [KeyboardButton("Перейти на сайт")],
                        [KeyboardButton("Назад")]]
    reply_markup = ReplyKeyboardMarkup(keyboard=contact_keyboard,
                                       resize_keyboard=True)
    context.bot.send_message(chat_id=update.message.from_user.id,
                             text="Супер, чим можем бути корисні?",
                             reply_markup=reply_markup)
    return ANSWER_MENU


def menu_answer_handler(update: Update, context: CallbackContext):
    if update.message.text == "Назад":
        contact_keyboard = [[KeyboardButton("Собака"),
                             KeyboardButton("Котик")],
                            [KeyboardButton("Собака та котик")]]
        reply_markup = ReplyKeyboardMarkup(keyboard=contact_keyboard,
                                           resize_keyboard=True)
        context.bot.send_message(chat_id=update.message.from_user.id,
                                 text="Хто Ваш улюбленець?",
                                 reply_markup=reply_markup)
        return MENU
    if update.message.text == "Перейти на сайт":
        inline_keyboard = [InlineKeyboardButton(
            text='Посилання', url='https://practik.ua/')],
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        context.bot.send_message(chat_id=update.message.from_user.id,
                                 text="Перейдіть будь ласка за посиланням.",
                                 reply_markup=inline_buttons)
        return MENU
