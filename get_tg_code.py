from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.types import BotCommand
from aiogram.filters import Command, CommandStart
import json


from aiogram.filters.callback_data import CallbackData

import settings


class ChooseBtn(CallbackData, prefix = 'any'):
    isTrue : bool


code_bot = Bot(token=settings.CODE_BOT_TOKEN)


async def set_commands(_bot: Bot):
    commands = [
        BotCommand(command='/start', description='Информация о боте'),
        BotCommand(command='/check', description='Узнать статус работы бота')
    ]
    await _bot.set_my_commands(commands=commands)


class BotManager:
    dp = Dispatcher()

    @staticmethod
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(
            text='Для отправки кода авторизации необходимо ввести сообщение с ключевым словом "code:"\n\n'
                 'Пример: code:123456')

    @staticmethod
    @dp.message(Command(commands='check'))
    async def process_check_status(message: Message):
        with open('auth_code.json', 'r') as code_json:
            data = json.load(code_json)

            if data['code'] == 'error':
                await message.answer(text='Статус авторизации: error')
            else:
                await message.answer(text='Ошибок при авторизации не обнаружено')

    @staticmethod
    @dp.message(lambda msg: 'code:' in msg.text)
    async def process_get_code(message: Message):
        global code
        code = message.text.split(':')[1].replace(' ', '')
        buttons = [
            [InlineKeyboardButton(text='Да', callback_data=ChooseBtn(isTrue=True).pack())],
            [InlineKeyboardButton(text='Нет', callback_data=ChooseBtn(isTrue=False).pack())]
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer(text=f'{message.text}\n\nПравильно ли вы ввели код?', reply_markup=keyboard)

    @staticmethod
    @dp.callback_query(ChooseBtn.filter())
    async def process_send_code(callback: CallbackQuery, callback_data: ChooseBtn):
        global code
        await callback.message.delete()
        if callback_data.isTrue:
            with open('auth_code.json', 'r+') as code_json:
                try:
                    data = json.load(code_json)
                except json.JSONDecodeError:
                    data = dict()
                data['code'] = code
                code_json.seek(0)
                json.dump(data, code_json)
                code_json.truncate()
        else:
            await callback.message.answer(text='Введите код снова')


if __name__ == '__main__':
    manager = BotManager()
    manager.dp.startup.register(set_commands)
    manager.dp.run_polling(code_bot)
