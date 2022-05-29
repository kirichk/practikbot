import os
from pathlib import Path
from datetime import time
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import (CallbackQueryHandler, Updater, MessageHandler,
                          CommandHandler, ConversationHandler, Filters)
from telegram.utils.request import Request
from telebot.handlers import (greetings_handler, phone_handler,
                              pet_handler, menu_handler, menu_answer_handler)
from loguru import logger

dotenv_path = os.path.join(Path(__file__).parent, 'config/.env')
load_dotenv(dotenv_path)

logger.add(
    "logs/info.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="100 MB",
    compression="zip",
)


TOKEN = os.getenv("TOKEN")
PET, PHONE, MENU, ANSWER_MENU = range(4)


@logger.catch
def main():
    '''Setting up all needed to launch bot'''
    logger.info('Started')

    req = Request(
        connect_timeout=30.0,
        read_timeout=5.0,
        con_pool_size=8,
    )
    bot = Bot(
        token=TOKEN,
        request=req,
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    # Проверить что бот корректно подключился к Telegram API
    info = bot.get_me()
    logger.info('Bot info: %s', info)

    # Навесить обработчики команд
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', greetings_handler),
            CallbackQueryHandler(greetings_handler,
                                 pattern=r'^start$',
                                 pass_user_data=True),
        ],
        states={
            PHONE: [MessageHandler(Filters.all, phone_handler,
                                   pass_user_data=True),
                    CommandHandler('start', greetings_handler)],
            PET: [MessageHandler(Filters.all, pet_handler,
                                 pass_user_data=True),
                  CommandHandler('start', greetings_handler)],
            MENU: [MessageHandler(Filters.all, menu_handler,
                                  pass_user_data=True),
                   CommandHandler('start', greetings_handler)],
            ANSWER_MENU: [MessageHandler(Filters.all, menu_answer_handler,
                                         pass_user_data=True),
                          CommandHandler('start', greetings_handler)],
        },
        fallbacks=[
            CommandHandler('start', greetings_handler),
        ],
    )
    updater.dispatcher.add_handler(conv_handler)
    # updater.dispatcher.add_handler(MessageHandler(Filters.all, echo_handler))
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=80,
    #                       url_path=TOKEN,
    #                       webhook_url="https://53ba-95-67-60-185.ngrok.io" + TOKEN)
    updater.start_polling()
    updater.idle()
    logger.info('Stopped')


if __name__ == '__main__':
    main()
