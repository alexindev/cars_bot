from aiogram import types, Dispatcher
from aiogram.filters import Command
from loader import bot


async def start_command(message: types.Message):
    """ Команда /start """
    await bot.send_message(message.from_user.id, text='старт')


async def help_command(message: types.Message):
    """ Команда /help """
    await bot.send_message(message.from_user.id, text='помощь')


def commands_handlers(dp: Dispatcher):
    """ Регистрация обработчиков """
    dp.message.register(start_command, Command(commands='start'))
    dp.message.register(help_command, Command(commands='help'))

