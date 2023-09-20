from keyboard.standart import register_kb
from keyboard.inline import main_kb
from loader import bot, base
from aiogram import types, Dispatcher
from aiogram.filters import Command


async def start_command(message: types.Message):
    """ Команда /start """
    user = base.get_user(chat_id=message.from_user.id)
    if user:
        await bot.send_message(message.from_user.id, 'Главная страница', reply_markup=main_kb())
    else:
        await bot.send_message(message.from_user.id, 'Необходима регистрация.\n'
                                                     'Для этого нажмите на кнопку ниже 👇',
                               reply_markup=register_kb)


async def help_command(message: types.Message):
    """ Команда /help """
    await bot.send_message(message.from_user.id, text='помощь')


def commands_handlers(dp: Dispatcher):
    """ Регистрация обработчиков """
    dp.message.register(start_command, Command(commands='start'))
    dp.message.register(help_command, Command(commands='help'))

