from aiogram import types, Dispatcher, F
from datetime import datetime

from keyboard.inline import statistic_kb, cancel_kb
from loader import data, base
from logs.config import logger
from utils.helpers import get_statistic_text


async def driver_statistic(callback: types.CallbackQuery):
    """ Меню статистики """
    await callback.answer()
    await callback.message.edit_text('Выберите пункт: 👇', reply_markup=statistic_kb())


async def detail_statistic(callback: types.CallbackQuery):
    """ Детальная статистика за интервал """
    await callback.answer()
    await callback.message.edit_text('⏳ Собираем статистику...')
    user = base.get_user(chat_id=callback.from_user.id)
    if user:
        interval = '01'
        callback_data = callback.data.split('_')[-1]
        date_to = datetime.today().strftime('%Y-%m-%d')
        date_from = datetime.today().strftime('%Y-%m-01')

        if callback_data == 'day':
            interval = datetime.now().strftime('%d')
            date_from = datetime.today().strftime('%Y-%m-%d')

        driver_id = user.get('driver_id')
        cancelled = data.get_canceled_trip(driver_id=driver_id, date_from=date_from, date_to=date_to,
                                           park_id=user.get('park_id'), session_id=user.get('session_id'))
        stat = data.get_status(driver_id=driver_id, interval=interval, park_id=user.get('park_id'),
                               session_id=user.get('session_id'))

        if stat:
            text = get_statistic_text(stat, cancelled)
            await callback.message.edit_text(text=text, reply_markup=cancel_kb())
        else:
            logger.error('Данные по статистике на найдены')
    else:
        await callback.message.edit_text('❌ Сначала зарегистрируйтесь /start', reply_markup=cancel_kb())


def statistics_handlers(dp: Dispatcher):
    dp.callback_query.register(driver_statistic, F.data == 'user_stat')
    dp.callback_query.register(detail_statistic,  F.data.startswith('stat_'))
