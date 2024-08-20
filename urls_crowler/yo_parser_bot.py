import threading
import time
import uvicorn
import telebot

import settings
from urls_crowler.run_crowlers import run_parser_for_bot

bot = telebot.TeleBot(settings.BOT_TOKEN)


class YOParserBot:
    def __init__(self):
        self.last_message_id = None
        self.in_process = False

        self.status_messages = [
            'Все обработанные ссылки храняться в кешэ, их не приходится заново обрабатывать.',
            'Бот не пришлёт тебе те вакансии, которые он тебе уже присылал.',
            'Бот не будет реагировать ни на какие сообщения пока обрабатывает вакансии.',
            'Бота могут запускать несколько юзеров одновременно и ничего не сломается.',
            'Даже наоборот, если один юзер наткнётся на новую ссылку, он тут же положит её в кеш,'
            ' и второй юзер достунет оттуда, а не станет обрабатывать сам.',
            'По окончанию процесса обработки тебе также пришлётся статистика.',
            'Статистика по дефолту состоит из трёх частей:\n'
            '1) Количество вакансий в файле.',
            '2) Время выполнения обработки.',
            '3) Скорость обработки вакансий в секунду.',
            'Скоро ты сможешь сам настроить интересующую тебя информацию.',
            'К примеру, сможешь получать ошибки, которые возникли в процессе обработки,'
            ' или же совсем откючить эти сообщения.',
            'Эти сообщения созданы для того, чтобы ты мог убедиться, что бот работает, а также узнать пару '
            'интересных фактов о нём.',
        ]
        self.start_message = 'Начал обработку'
        self.finish_message = 'Закончил обработку вакансий, надеюсь ты обрадуешься результату, жду тебя снова!'
        self.current_message_index = 0

    def update_status(self, chat_id):
        self.current_message_index = (self.current_message_index + 1) % len(self.status_messages)
        message_text = self.status_messages[self.current_message_index]
        bot.edit_message_text(chat_id=chat_id, message_id=self.last_message_id, text=message_text)

    def finish_status(self, chat_id):
        self.current_message_index = (self.current_message_index + 1) % len(self.status_messages)
        bot.edit_message_text(chat_id=chat_id, message_id=self.last_message_id, text=self.finish_message)

    def get_progress(self):
        return self.in_process

    def set_progress(self, in_process):
        self.in_process = in_process

    @staticmethod
    def make_message_from_data(result_message):
        return (f'Всего вакансий: {result_message.all_links_count}\n'
                f'Всего времени: {result_message.time_spent}\n'
                f'Скорость: {result_message.av_speed} вакансий/сек')

    def start_processing(self, chat_id):
        self.set_progress(True)
        bot.send_message(chat_id, self.start_message)
        self.last_message_id = bot.send_message(chat_id, self.status_messages[0]).message_id

        def run_parser_and_send_result():
            result_message = run_parser_for_bot(chat_id)
            self.set_progress(False)
            bot.send_document(chat_id, open(settings.FILE_NAME, 'rb'))
            bot.send_message(chat_id, self.make_message_from_data(result_message))

        parser_thread = threading.Thread(target=run_parser_and_send_result)
        parser_thread.start()

        while self.get_progress():
            time.sleep(6)
            self.update_status(chat_id)
        self.finish_status(chat_id)
        users_running.remove(chat_id)

        parser_thread.join()


users_running = []
@bot.message_handler(commands=['start'])
def start(update):
    chat_id = update.from_user.id
    if chat_id not in users_running:
        yo_instance = YOParserBot()
        users_running.append(chat_id)
        yo_instance.start_processing(chat_id)



def _run_bot():
    bot.polling(none_stop=True)


def run_bot():
    thread = threading.Thread(target=_run_bot)
    thread.daemon = True
    thread.start()


if __name__ == '__main__':
    uvicorn.run(run_bot, host='0.0.0.0', port=8001)
