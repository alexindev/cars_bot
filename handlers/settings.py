from aiogram import types, Dispatcher, F
from loader import data, base
from keyboard.inline import settings_kb, delivery_settings_kb, cancel_kb, incity_settings_kb
from utils.helpers import get_state_text


async def settings_user(callback: types.CallbackQuery):
    """ Настройки пользователя """
    await callback.answer()
    await callback.message.edit_text('Выберите пункт: 👇', reply_markup=settings_kb())


async def current_state(callback: types.CallbackQuery):
    """ Текущее состояние профиля """
    await callback.answer()
    user = base.get_user(chat_id=callback.from_user.id)
    if user:
        car_id = user.get('car_id')
        state = data.get_current_state(car_id)
        if state:
            text = get_state_text(state)
            await callback.message.edit_text(text=text, reply_markup=cancel_kb())
        else:
            await callback.message.edit_text('❌ Ошибка получения данных', reply_markup=cancel_kb())
    else:
        await callback.message.edit_text('❌ Ошибка получения пользователя', reply_markup=cancel_kb())


async def delivery_settings(callback: types.CallbackQuery):
    """ Настройки режима доставки """
    await callback.answer()
    await callback.message.edit_text('Выберите действие: 👇', reply_markup=delivery_settings_kb())


async def delivery_manager(callback: types.CallbackQuery):
    """ Управление режимом доставки """
    await callback.answer()
    callback_data = callback.data.split('_')[-1]
    category = ['express', 'courier']
    user = base.get_user(chat_id=callback.from_user.id)
    if user:
        car_id = user.get('car_id')
        state: dict = data.get_current_state(car_id=car_id)
        if state:
            categories = state.get('categories')
            if callback_data == 'on':
                if 'express' in categories:
                    await callback.message.edit_text('🤝 Доставка уже включена', reply_markup=cancel_kb())
                else:
                    state['categories'].extend(category)
                    state['amenities'].append('delivery')
                    status = data.update_category(car_id, state)
                    if status:
                        await callback.message.edit_text('✅ Доставка включена', reply_markup=cancel_kb())
                    else:
                        await callback.message.edit_text('❌ Ошибка изменения данных', reply_markup=cancel_kb())
            else:
                if 'express' in categories:
                    for elem in category:
                        if elem in state['categories']:
                            state['categories'].remove(elem)
                    state['amenities'].remove('delivery')
                    status = data.update_category(car_id, state)
                    if status:
                        await callback.message.edit_text('✅ Доставка выключена', reply_markup=cancel_kb())
                    else:
                        await callback.message.edit_text('❌ Ошибка изменения данных', reply_markup=cancel_kb())
                else:
                    await callback.message.edit_text('💔 Доставка уже выключена', reply_markup=cancel_kb())
        else:
            await callback.message.edit_text('❌ Ошибка получения данных', reply_markup=cancel_kb())
    else:
        await callback.message.edit_text('❌ Ошибка получения пользователя', reply_markup=cancel_kb())


async def incity_settings(callback: types.CallbackQuery):
    """ Настройки режима Межгород """
    await callback.answer()
    await callback.message.edit_text('Выберите действие: 👇', reply_markup=incity_settings_kb())


async def incity_manager(callback: types.CallbackQuery):
    """ Управление режимом Межгород """
    await callback.answer()
    callback_data = callback.data.split('_')[-1]

    category = ['intercity']
    user = base.get_user(chat_id=callback.from_user.id)
    if user:
        car_id = user.get('car_id')
        state: dict = data.get_current_state(car_id=car_id)
        if state:
            categories = state.get('categories')
            if callback_data == 'on':
                if 'intercity' in categories:
                    await callback.message.edit_text('🤝 Поездки по межгороду уже включен', reply_markup=cancel_kb())
                else:
                    state['categories'].extend(category)
                    status = data.update_category(car_id, state)
                    if status:
                        await callback.message.edit_text('✅ Поездки по межгороду включены', reply_markup=cancel_kb())
                    else:
                        await callback.message.edit_text('❌ Ошибка изменения данных', reply_markup=cancel_kb())
            else:
                if 'intercity' in categories:
                    state['categories'].remove('intercity')
                    status = data.update_category(car_id, state)
                    if status:
                        await callback.message.edit_text('✅ Поездки по межгороду выключены', reply_markup=cancel_kb())
                    else:
                        await callback.message.edit_text('❌ Ошибка изменения данных', reply_markup=cancel_kb())
                else:
                    await callback.message.edit_text('💔 Поездки по межгороду уже выключены', reply_markup=cancel_kb())
        else:
            await callback.message.edit_text('❌ Ошибка получения данных', reply_markup=cancel_kb())
    else:
        await callback.message.edit_text('❌ Ошибка получения пользователя', reply_markup=cancel_kb())


def settings_handlers(dp: Dispatcher):
    dp.callback_query.register(settings_user, F.data == 'settings')
    dp.callback_query.register(current_state, F.data == 'current_state')
    dp.callback_query.register(delivery_settings, F.data == 'delivery')
    dp.callback_query.register(delivery_manager, F.data.startswith('delivery_'))
    dp.callback_query.register(incity_settings, F.data == 'incity')
    dp.callback_query.register(incity_manager, F.data.startswith('incity_'))

