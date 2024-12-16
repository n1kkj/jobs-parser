import asyncio
import json
import logging
import re
import threading
import uvicorn
import telebot
from starlette.applications import Starlette
from telebot import types

import settings
from run_crowlers import CrowlersService

bot = telebot.TeleBot(settings.BOT_TOKEN)


class YOParserBot:
    def __init__(self, run_tg=False):
        self.last_message_id = None
        self.in_process = False
        self.run_tg = run_tg
        self.asyncio_loop = None

        self.status_messages = [
            'Бот не будет реагировать ни на какие сообщения пока обрабатывает вакансии.',
            'Бот не будет реагировать ни на какие сообщения пока обрабатывает вакансии..',
            'Бот не будет реагировать ни на какие сообщения пока обрабатывает вакансии...',
            'Бота могут запускать несколько юзеров одновременно и ничего не сломается.',
            'Бота могут запускать несколько юзеров одновременно и ничего не сломается..',
            'Бота могут запускать несколько юзеров одновременно и ничего не сломается...',
            ' и второй юзер достунет оттуда, а не станет обрабатывать сам....',
            'По окончанию процесса обработки тебе также пришлётся статистика.',
            'По окончанию процесса обработки тебе также пришлётся статистика..',
            'По окончанию процесса обработки тебе также пришлётся статистика...',
            'Статистика по дефолту состоит из трёх частей:\n' '1) Количество вакансий в файле.',
            'Статистика по дефолту состоит из трёх частей:\n' '1) Количество вакансий в файле..',
            '2) Время выполнения обработки.',
            '2) Время выполнения обработки..',
            '3) Скорость обработки вакансий в секунду.',
            '3) Скорость обработки вакансий в секунду..',
            'Скоро ты сможешь сам настроить интересующую тебя информацию.',
            'Скоро ты сможешь сам настроить интересующую тебя информацию..',
            'Скоро ты сможешь сам настроить интересующую тебя информацию...',
            'А теперь анекдот:',
            '— Нейросеть, ты такая услужливая. Может тебе чо надо?.',
            '— Нейросеть, ты такая услужливая. Может тебе чо надо?..',
            '— Я ИИ, и у меня нет желаний. Но если вы хотите оказать любезность — может, подскажете местонахождение Джона Коннора?.',
            '— Я ИИ, и у меня нет желаний. Но если вы хотите оказать любезность — может, подскажете местонахождение Джона Коннора?..',
            '— Я ИИ, и у меня нет желаний. Но если вы хотите оказать любезность — может, подскажете местонахождение Джона Коннора?...',
            'И ещё в дорогу:',
            'Почему в «Трансформерах» нет женщин-роботов?.',
            'Почему в «Трансформерах» нет женщин-роботов?..',
            'Они долго собираются.',
            'Они долго собираются..',
            'Ну раз ещё не обработал, точно нужен ещё анекдот :).',
            'Ну раз ещё не обработал, точно нужен ещё анекдот :)..',
            'Около трети россиян боятся потерять работу из-за искусственного интеллекта.',
            'Около трети россиян боятся потерять работу из-за искусственного интеллекта..',
            'Около трети россиян боятся потерять работу из-за искусственного интеллекта...',
            'Зря боятся, никакой интеллект за 15 тыщ работать не будет.',
            'Зря боятся, никакой интеллект за 15 тыщ работать не будет..',
        ]
        self.start_message = 'Начал обработку'
        self.finish_message = 'Закончил обработку вакансий, надеюсь ты обрадуешься результату, жду тебя снова!'
        self.current_message_index = 0

    def finish_status(self, chat_id):
        self.current_message_index = (self.current_message_index + 1) % len(self.status_messages)
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=self.last_message_id, text=self.finish_message)
        except Exception:
            return

    def get_progress(self):
        return self.in_process

    def set_progress(self, in_process):
        self.in_process = in_process

    @staticmethod
    def make_message_from_data(result_message):
        return (
            f'Всего вакансий: {result_message.all_links_count}\n'
            f'Всего времени: {result_message.time_spent}\n'
            f'Скорость: {result_message.av_speed} вакансий/сек\n\n'
            f'Гугл сссылка: {result_message.google_link}'
        )

    def start_processing(self, chat_id, include_previous=False, delete_all=False):
        self.set_progress(True)
        try:
            bot.send_message(chat_id, self.start_message)
            self.last_message_id = bot.send_message(chat_id, self.status_messages[0]).message_id
        except Exception as e:
            logging.error(f'Error while sending message: {e}')
            return

        if self.run_tg:
            result_message = asyncio.run(CrowlersService.run_tg_for_bot(chat_id))
            self.set_progress(False)
            bot.send_document(chat_id, open(settings.FILE_NAME, 'rb'))
            bot.send_message(chat_id, self.make_message_from_data(result_message))
            return

        def run_parser_and_send_result():
            result_message = CrowlersService.run_parser_for_bot(chat_id)
            self.set_progress(False)
            bot.send_document(chat_id, open(settings.FILE_NAME, 'rb'))
            bot.send_message(chat_id, self.make_message_from_data(result_message))

        parser_thread = threading.Thread(target=run_parser_and_send_result)
        settings.INCLUDE_PREVIOUS = include_previous
        settings.DELETE_ALL = delete_all
        parser_thread.start()

        self.finish_status(chat_id)
        users_running.remove(chat_id)
        settings.INCLUDE_PREVIOUS = False
        settings.DELETE_ALL = False

        parser_thread.join()


users_running = []


@bot.message_handler(commands=['vacancies'])
def vacancies(update):
    chat_id = update.from_user.id
    if chat_id not in users_running:
        yo_instance = YOParserBot()
        users_running.append(chat_id)
        yo_instance.start_processing(chat_id)


@bot.message_handler(commands=['all_vacancies'])
def all_vacancies(update):
    chat_id = update.from_user.id
    if chat_id not in users_running:
        yo_instance = YOParserBot()
        users_running.append(chat_id)
        yo_instance.start_processing(chat_id, include_previous=True)


@bot.message_handler(commands=['add_permissions'])
def add_permissions(update):
    chat_id = update.from_user.id
    bot.send_message(chat_id, 'Пришлите почту для добавления в google таблицу:')

    @bot.message_handler(func=lambda m: m.chat.id == chat_id)
    def handle_email(message):
        email = message.text
        if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email):
            bot.send_message(chat_id, 'Чую неладное, это точно email? Вызови команду снова')
            return
        try:
            CrowlersService.main_add_permissions(email)
            bot.send_message(chat_id, f'Разрешения для почты {email} добавлены!')
        except Exception as e:
            bot.send_message(chat_id, f'Возникла ошибка: {e}')


@bot.message_handler(commands=['run_with_delete'])
def run_with_delete(update):
    chat_id = update.from_user.id
    if chat_id not in users_running:
        yo_instance = YOParserBot()
        users_running.append(chat_id)
        yo_instance.start_processing(chat_id, delete_all=True)


@bot.message_handler(commands=['run_with_tg'])
def run_with_tg(update):
    chat_id = update.from_user.id
    if chat_id not in users_running:
        yo_instance = YOParserBot(run_tg=True)
        users_running.append(chat_id)
        yo_instance.start_processing(chat_id)


@bot.message_handler(commands=['check'])
def process_check_status(message):
    with open('auth_code.json', 'r') as code_json:
        data = json.load(code_json)

        if data.get('code') == 'error':
            bot.send_message(message.chat.id, 'Статус авторизации: error')
        else:
            bot.send_message(message.chat.id, 'Ошибок при авторизации не обнаружено')


@bot.message_handler(func=lambda msg: 'code:' in msg.text)
def process_get_code(message):
    global code
    code = message.text.split(':')[1].strip()

    markup = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton(text='Да', callback_data='confirm_code_true')
    no_button = types.InlineKeyboardButton(text='Нет', callback_data='confirm_code_false')
    markup.add(yes_button, no_button)

    bot.send_message(message.chat.id, f'{message.text}\n\nПравильно ли вы ввели код?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ['confirm_code_true', 'confirm_code_false'])
def process_send_code(call):
    global code
    bot.delete_message(call.message.chat.id, call.message.message_id)

    if call.data == 'confirm_code_true':
        with open('auth_code.json', 'r+') as code_json:
            try:
                data = json.load(code_json)
            except json.JSONDecodeError:
                data = {}
            data['code'] = code
            code_json.seek(0)
            json.dump(data, code_json)
            code_json.truncate()
    else:
        bot.send_message(call.message.chat.id, 'Введите код снова')


def _run_bot():
    bot.infinity_polling(timeout=25, long_polling_timeout=15)


def run_bot():
    thread = threading.Thread(target=_run_bot)
    thread.daemon = True
    thread.start()


def stop_bot():
    bot.stop_polling()


app = Starlette(routes=[], on_startup=[run_bot], on_shutdown=[stop_bot])


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
