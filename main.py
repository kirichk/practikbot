from flask import Flask, request, Response, json, jsonify
from multiprocessing import Process
# from telegrambot import main as tgbot
# from vibertelebot import main as vbbot
from db_func.database import create_table
from loguru import logger
from tasks.task import task_checker
from telebot import main as tgbot


app = Flask(__name__)


# @app.route('/viber', methods=['POST'])
# def viber_endpoint():
#     source = 'viber'
#     vbbot.main(request)
#     return Response(status=200)


if __name__ == '__main__':
    # flask_server = Process(target=server_launch).start()
    # telegram_bot = Process(target=tgbot.main).start()
    create_table()
    try:
        background_process = Process(target=task_checker).start()
        # flask_server = Process(target=server_launch).start()
        telegram_bot = Process(target=tgbot.main).start()
    except KeyboardInterrupt:
        # flask_server.terminate()
        telegram_bot.terminate()
        background_process.terminate()
        # flask_server.join()
        telegram_bot.join()
        background_process.join()
