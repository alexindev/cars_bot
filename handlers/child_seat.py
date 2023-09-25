from aiogram import types

from keyboard.inline import seat_settings_kb, cancel_kb, seats_kb
from loader import data, base
from utils.browser import driver
from utils.helpers import get_seat_text


async def seat_settings(callback: types.CallbackQuery):
    """ Настройки детского кресла """
    await callback.answer()
    await callback.message.edit_text('Выберите действие: 👇', reply_markup=seat_settings_kb())


async def seat_info(callback: types.CallbackQuery):
    """ Информация о детском кресле """
    await callback.answer()
    user = base.get_user(chat_id=callback.from_user.id)
    if user:
        car_id = user.get('car_id')
        state: dict = data.get_current_state(car_id=car_id)
        if state:
            if 'chairs' in state:
                seats = []
                for i in state.get('chairs'):
                    seats.extend(i.get('categories'))
                text = get_seat_text(seats)
                await callback.message.edit_text(text=text, reply_markup=cancel_kb())
            else:
                await callback.message.edit_text('🗿 Ни одного детского кресла не добавлено',
                                                 reply_markup=cancel_kb())
    else:
        await callback.message.edit_text('❌ Сначала зарегистрируйтесь /start', reply_markup=cancel_kb())


async def seat_add(callback: types.CallbackQuery):
    """ Выбрать категорию кресла для добавления """
    await callback.answer()
    await callback.message.edit_text('Выберите категорию для добавления: 👇', reply_markup=seats_kb('add'))


async def seat_delete(callback: types.CallbackQuery):
    """ Выбрать категорию кресла для удаления """
    await callback.answer()
    await callback.message.edit_text('Выберите категорию для удаления: 👇', reply_markup=seats_kb('delete'))


async def seat_update(callback: types.CallbackQuery):
    """ Управление детскими креслами """
    await callback.answer()
    user = base.get_user(chat_id=callback.from_user.id)
    if user:
        callback_data = callback.data.split('__')[-1]

        action = 'create'
        if callback_data.startswith('add'):
            category = callback_data.split('_')[-1]
        else:
            action = 'delete'
            category = callback_data.split('_')[-1]
        await callback.message.edit_text('⏳ Ожидаем выполнение операции...')
        seat = await driver(driver_id=user.get('driver_id'), action=action, category=category)
        if seat:
            await callback.message.edit_text('✅ Успешная операция', reply_markup=cancel_kb())
        else:
            await callback.message.edit_text('❌ Ошибка при выполнении операции', reply_markup=cancel_kb())
    else:
        await callback.message.edit_text('❌ Сначала зарегистрируйтесь /start', reply_markup=cancel_kb())

