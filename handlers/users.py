from aiogram import types, Dispatcher, F
from aiogram.types import ReplyKeyboardRemove

from keyboard.inline import main_kb, cancel_kb
from keyboard.standart import register_kb
from loader import bot, data, base
from utils.helpers import get_leaderboard_text


async def authorization_user(message: types.Message):
    """
    Регистрация/авторизация пользователей

    Если номер телефона найден в парке, регистрируем
    """
    phone = message.contact.phone_number
    if phone:
        if not phone.startswith('+'):
            phone = '+' + phone
        check_message = await bot.send_message(
            message.from_user.id,
            '🔍 Проверяем номер телефона...',
            reply_markup=ReplyKeyboardRemove()
        )
        driver_id = data.get_driver_id_by_phone(phone)
        if driver_id:
            base.register_user(message.from_user.id, phone, driver_id)
            # возможна дополнительная логика с оповещение о регистрации
            await bot.delete_message(message.from_user.id, check_message.message_id)
            await bot.send_message(
                chat_id=message.from_user.id,
                text='Главное меню',
                reply_markup=main_kb()
            )
        else:
            await bot.delete_message(message.from_user.id, check_message.message_id)
            await bot.send_message(
                chat_id=message.from_user.id,
                text='❌ Номер в базе не найден\n\n'
                     '⚡ Зарегистрироваться в парке можно на сайте волжский21.рф или напишите https://t.me/',
                reply_markup=register_kb
            )
    else:
        await bot.send_message(message.from_user.id, 'Номер телефона не получен')


async def current_order(callback: types.CallbackQuery):
    """ Текущий заказ """
    await callback.message.edit_text('🤷‍♀ На данный момент нет активных заказов', reply_markup=cancel_kb())
    await callback.answer()


async def liderboard(callback: types.CallbackQuery):
    """ Таблица лидеров """
    liders: list = data.get_leaders()
    if liders:
        text = get_leaderboard_text(liders)
        await callback.message.edit_text(text, reply_markup=cancel_kb())
    else:
        await callback.message.edit_text('Таблица лидеров на данный момент не сформирована',
                                         reply_markup=cancel_kb())
    await callback.answer()


async def cancel_menu(callback: types.CallbackQuery):
    """ Возврат в главное меню """
    await callback.message.edit_text('Главная страница', reply_markup=main_kb())
    await callback.answer()


def user_hanlers(dp: Dispatcher):
    """ Регистрация обработчиков """
    dp.message.register(authorization_user, F.contact)
    dp.callback_query.register(current_order, F.data == 'current_order')
    dp.callback_query.register(liderboard, F.data == 'leaderboard')
    dp.callback_query.register(cancel_menu, F.data == 'cancel')
