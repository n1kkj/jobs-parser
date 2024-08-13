import threading
import telebot

import settings
from run_crowlers import run_parser_for_bot

bot = telebot.TeleBot(settings.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(start_message, file_name=settings.FILE_NAME):
    bot.send_message(start_message.from_user.id, 'Начал обработку')
    run_parser_for_bot()
    bot.send_document(start_message.from_user.id, open(file_name, 'rb'))


def _run_bot():
    bot.polling(none_stop=True)


thread = threading.Thread(target=_run_bot)
thread.daemon = True
thread.start()
