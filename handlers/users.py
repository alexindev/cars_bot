from aiogram import types, Dispatcher, F
from loader import bot, base


async def register_user(message: types.Message):
    """ Регистрация пользователей """
    if message.contact.phone_number:
        base.register_user(message.from_user.id, message.contact.phone_number)
        await bot.send_message(message.from_user.id, 'Регистрация выполнена, нажмите на команду 👉 /start')
    else:
        await bot.send_message(message.from_user.id, 'Номер телефона не получен')


def user_hanlers(dp: Dispatcher):
    """ Регистрация обработчиков """
    dp.message.register(register_user, F.contact)
