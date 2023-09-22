from aiogram import types, Dispatcher, F

from keyboard.inline import settings_kb, seat_settings_kb, payment_settings_kb, delivery_settings_kb


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


def settings_handlers(dp: Dispatcher):
    dp.callback_query.register(settings_user, F.data == 'settings')
    dp.callback_query.register(seat_settings, F.data == 'seat')
    dp.callback_query.register(payment_settings, F.data == 'payment')
    dp.callback_query.register(delivery_settings, F.data == 'delivery')
