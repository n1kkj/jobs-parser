import threading
import uvicorn
import telebot

import settings
from run_crowlers import run_parser_for_bot

bot = telebot.TeleBot(settings.BOT_TOKEN)


class YOParserBot:
    in_process = False
    waiting_messages = [
        'Подожди, я в процессе, не отвлекай',
        'Я же попросил',
        '..ну зачем ты так?',
        'Уже скоро, потерпи',
        'Прям чуточку, важный момент, дай подумать',
        'Скоро будут тебе вакансии, много вакансий, честно честно',
        'Я всё Никите расскажу!',
    ]
    waiting_messages_index = 0

    @classmethod
    def get_progress(cls):
        return cls.in_process

    @classmethod
    def set_progress(cls, in_process):
        cls.in_process = in_process


@bot.message_handler(commands=['start'])
def start(start_message, file_name=settings.FILE_NAME):
    if not YOParserBot.get_progress():
        YOParserBot.set_progress(True)
        bot.send_message(start_message.from_user.id, 'Начал обработку')
        run_parser_for_bot()
        bot.send_document(start_message.from_user.id, open(file_name, 'rb'))
    else:
        bot.send_message(start_message.from_user.id, YOParserBot.waiting_messages[YOParserBot.waiting_messages_index])
        if YOParserBot.waiting_messages_index == len(YOParserBot.waiting_messages) - 1:
            YOParserBot.waiting_messages_index = 0
        else:
            YOParserBot.waiting_messages_index += 1


def _run_bot():
    bot.polling(none_stop=True)


def run_bot():
    thread = threading.Thread(target=_run_bot)
    thread.daemon = True
    thread.start()


if __name__ == '__main__':
    uvicorn.run(run_bot, host='0.0.0.0', port=8001)
