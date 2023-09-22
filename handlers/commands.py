from loader import bot
from aiogram import types, Dispatcher, F

from keyboard.standart import register_kb, send_phone_kb
from utils.text_answer import start_command_text, register_user_text, auth_user_text, park_info_text


async def start_command(message: types.Message):
    """ Стартовое сообщение """
    await bot.send_message(message.from_user.id, text=start_command_text, reply_markup=register_kb)


async def register_user(message: types.Message):
    """ Регистрация пользователей """
    await bot.send_message(message.from_user.id, text=register_user_text)


async def auth_user(message: types.Message):
    """ Авторизация пользователей """
    await bot.send_message(message.from_user.id, text=auth_user_text, reply_markup=send_phone_kb)


async def park_info(message: types.Message):
    """ Информация о парке """
    await bot.send_message(message.from_user.id, text=park_info_text)


def commands_handlers(dp: Dispatcher):
    """ Регистрация обработчиков """
    dp.message.register(start_command, (F.text == '↩ Отмена') | (F.text == '/start'))
    dp.message.register(register_user, F.text == '🚖 Стать водитилем | курьером')
    dp.message.register(auth_user, F.text == '🔑 Авторизация')
    dp.message.register(park_info, F.text == 'ℹ Информация о парке')
