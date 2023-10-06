from aiogram import types, Dispatcher, F
from aiogram.types import ReplyKeyboardRemove

from keyboard.inline import main_kb, cancel_kb
from keyboard.standart import register_kb
from loader import bot, data, base
from utils.helpers import get_leaderboard_text, get_quality_text, current_order_data, unpaid_orders_text
from utils.text_answer import main_menu, information_tex


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
        user = base.get_user(phone=phone)
        if user:
            await bot.delete_message(message.from_user.id, check_message.message_id)
            await bot.send_message(
                chat_id=message.from_user.id,
                text=main_menu,
                reply_markup=main_kb()
            )
        else:
            park_data = base.get_parks()
            for park in park_data:
                api_key = park.get('api_key')
                park_id = park.get('park_id')
                client = park.get('client')
                print(park.get('name'))
                driver = await data.get_driver_list(phone=phone, api_key=api_key, park_id=park_id, client=client)

                if driver:
                    base.register_user(chat_id=message.from_user.id, phone=phone, driver_id=driver[0], car_id=driver[1],
                                       park_id=park.get('id'), full_name=driver[2])
                    await bot.delete_message(message.from_user.id, check_message.message_id)
                    await bot.send_message(
                        chat_id=message.from_user.id,
                        text='✅ Регистрация выполнена'
                    )
                    await bot.send_message(
                        chat_id=message.from_user.id,
                        text=main_menu,
                        reply_markup=main_kb()
                    )
                    break
            else:
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text='❌ Номер в базе не найден\n\n'
                         '⚡ Зарегистрироваться в парке можно на сайте www или напишите https://t.me/',
                    reply_markup=register_kb
                )
    else:
        await bot.send_message(message.from_user.id, 'Номер телефона не получен')


async def liderboard(callback: types.CallbackQuery):
    """ Таблица лидеров """
    await callback.answer()

    user = base.get_user(chat_id=callback.from_user.id)
    if user:
        liders = await data.get_leaders(park_id=user.get('park_id'), session_id=user.get('session_id'))
        if liders:
            text = get_leaderboard_text(liders)
            await callback.message.edit_text(text, reply_markup=cancel_kb())
        else:
            await callback.message.edit_text('Таблица лидеров на данный момент не сформирована',
                                             reply_markup=cancel_kb())
    else:
        await callback.message.edit_text('❌ Сначала зарегистрируйтесь /start', reply_markup=cancel_kb())


async def quality(callback: types.CallbackQuery):
    """ Показатель качества водителя """
    await callback.answer()
    user = base.get_user(chat_id=callback.from_user.id)
    if user:
        quality_data = await data.get_quality(driver_id=user.get('driver_id'), park_id=user.get('park_id'),
                                              session_id=user.get('session_id'))
        if quality_data:
            text = get_quality_text(quality_data)
            await callback.message.edit_text(text=text, reply_markup=cancel_kb())
        else:
            await callback.message.edit_text(
                text='🙅 Недостаточно данных для определения качества за прошлую неделю',
                reply_markup=cancel_kb()
            )
    else:
        await callback.message.edit_text('❌ Сначала зарегистрируйтесь /start', reply_markup=cancel_kb())


async def current_order(callback: types.CallbackQuery):
    """ Текущий заказ """
    await callback.answer()

    user = base.get_user(chat_id=callback.from_user.id)
    if user:
        driver_id = user.get('driver_id')
        order = await data.get_current_order_status(driver_id=driver_id, park_id=user.get('park_id'),
                                                    session_id=user.get('session_id'))
        text = current_order_data(data=order, status=user.get('is_staff'))
        await callback.message.edit_text(text=text, reply_markup=cancel_kb())
    else:
        await callback.message.edit_text('❌ Сначала зарегистрируйтесь /start', reply_markup=cancel_kb())


async def unpaid_orders(callback: types.CallbackQuery):
    """ Неоплаченные заказы """
    await callback.answer()
    user = base.get_user(chat_id=callback.from_user.id)
    if user:
        await callback.message.edit_text('🔎 Собираем информацию...')
        result = await data.get_unpaid_orders(driver_id=user.get('driver_id'), park_id=user.get('park_id'),
                                              session_id=user.get('session_id'))
        text = unpaid_orders_text(data=result)
        await callback.message.edit_text(text=text, reply_markup=cancel_kb())
    else:
        await callback.message.edit_text('❌ Сначала зарегистрируйтесь /start', reply_markup=cancel_kb())


async def information(callback: types.CallbackQuery):
    """ Ответы на частые вопросы """
    await callback.answer()
    await callback.message.edit_text(information_tex, reply_markup=cancel_kb())


async def cancel_menu(callback: types.CallbackQuery):
    """ Возврат в главное меню """
    await callback.answer()
    await callback.message.edit_text(main_menu, reply_markup=main_kb())


def user_handlers(dp: Dispatcher):
    """ Регистрация обработчиков """
    dp.message.register(authorization_user, F.contact)
    dp.callback_query.register(liderboard, F.data == 'leaderboard')
    dp.callback_query.register(quality, F.data == 'quality')
    dp.callback_query.register(current_order, F.data == 'current_order')
    dp.callback_query.register(unpaid_orders, F.data == 'unpaid_orders')
    dp.callback_query.register(information, F.data == 'information')
    dp.callback_query.register(cancel_menu, F.data == 'cancel')
