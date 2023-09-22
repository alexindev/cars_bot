from aiogram import types, Dispatcher, F
from aiogram.types import ReplyKeyboardRemove

from keyboard.inline import settings_kb, seat_settings_kb, payment_settings_kb, delivery_settings_kb, main_kb, \
    statistic_kb, cancel_kb
from loader import bot, base, data


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
        await bot.send_message(message.from_user.id, 'Номер телефона не получен')


async def current_order(callback: types.CallbackQuery):
    """ Текущий заказ """
    await callback.message.edit_text('🤷‍♀ На данный момент нет активных заказов', reply_markup=cancel_kb())
    await callback.answer()


async def liderboard(callback: types.CallbackQuery):
    """ Таблица лидеров """
    liders: list = data.get_leaders()
    if liders:
        text = ''
        for i, lider in enumerate(liders[:3], start=1):
            fullname, orders = lider.split()[:2], lider.split()[-1]
            medal = '🥇' if i == 1 else '🥈' if i == 2 else '🥉'
            text += f'{medal} {" ".join(fullname)} - {orders} заказов\n'

        if len(liders) >= 4:
            for lider in liders[3:]:
                fullname, orders = lider.split()[:2], lider.split()[-1]
                text += f'🎗 {" ".join(fullname)} - {orders} заказов\n'

        await callback.message.edit_text(text, reply_markup=cancel_kb())
    else:
        await callback.message.edit_text('Таблица лидеров на данный момент не сформирована',
                                         reply_markup=cancel_kb())
    await callback.answer()


async def driver_statistic(callback: types.CallbackQuery):
    """ Статистика водителя """
    await callback.message.edit_text('Выберите пункт: 👇', reply_markup=statistic_kb())
    await callback.answer()


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
    dp.callback_query.register(current_order, F.data == 'current_order')
    dp.callback_query.register(liderboard, F.data == 'leaderboard')
    dp.callback_query.register(driver_statistic, F.data == 'user_stat')
    dp.callback_query.register(settings_user, F.data == 'settings')
    dp.callback_query.register(seat_settings, F.data == 'seat')
    dp.callback_query.register(payment_settings, F.data == 'payment')
    dp.callback_query.register(delivery_settings, F.data == 'delivery')
    dp.callback_query.register(cancel_menu, F.data == 'cancel')
