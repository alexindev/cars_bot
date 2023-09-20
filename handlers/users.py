from aiogram import types, Dispatcher, F
from aiogram.types import ReplyKeyboardRemove

from keyboard.inline import settings_kb, seat_settings_kb, payment_settings_kb, delivery_settings_kb, main_kb
from loader import bot, base


async def register_user(message: types.Message):
    """ Регистрация пользователей """
    if message.contact.phone_number:
        base.register_user(message.from_user.id, message.contact.phone_number)
        await bot.send_message(
            message.from_user.id,
            'Регистрация выполнена, нажмите на команду 👉 /start',
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await bot.edit_message_text(message.from_user.id, message.message_id, 'Номер телефона не получен')


async def settings_user(callback: types.CallbackQuery):
    """ Настройки пользователя """
    await callback.message.edit_text('Выберите пункт: 👇', reply_markup=settings_kb())
    await callback.answer()


async def seat_settings(callback: types.CallbackQuery):
    """ Настройки детского кресла """
    await callback.message.edit_text('Выберите действие: 👇', reply_markup=seat_settings_kb())
    await callback.answer()


async def payment_settings(callback: types.CallbackQuery):
    """ Настройки режима оплаты """
    await callback.message.edit_text('Выберите действие: 👇', reply_markup=payment_settings_kb())
    await callback.answer()


async def delivery_settings(callback: types.CallbackQuery):
    """ Настройки режима доставки """
    await callback.message.edit_text('Выберите действие: 👇', reply_markup=delivery_settings_kb())
    await callback.answer()


async def cancel_menu(callback: types.CallbackQuery):
    """ Возврат в главное меню """
    await callback.message.edit_text('Главная страница', reply_markup=main_kb())
    await callback.answer()


def user_hanlers(dp: Dispatcher):
    """ Регистрация обработчиков """
    dp.message.register(register_user, F.contact)
    dp.callback_query.register(settings_user, F.data == 'settings')
    dp.callback_query.register(seat_settings, F.data == 'seat')
    dp.callback_query.register(payment_settings, F.data == 'payment')
    dp.callback_query.register(delivery_settings, F.data == 'delivery')
    dp.callback_query.register(cancel_menu, F.data == 'cancel')
