from aiogram import types, Dispatcher, F
from datetime import datetime

from keyboard.inline import statistic_kb, cancel_kb
from loader import data, base
from logs.config import logger
from utils.helpers import get_statistic_text


async def driver_statistic(callback: types.CallbackQuery):
    """ Меню статистики """
    await callback.message.edit_text('Выберите пункт: 👇', reply_markup=statistic_kb())
    await callback.answer()


async def detail_statistic(callback: types.CallbackQuery):
    """ Детальная статистика за интервал """
    user = base.get_user(chat_id=callback.from_user.id)
    if user:
        interval = '01'
        callback_data = callback.data.split('_')[-1]
        if callback_data == 'day':
            interval = datetime.now().strftime('%d')
        driver_id = user.get('driver_id')
        stat = data.get_status(driver_id, interval)
        if stat:
            text = get_statistic_text(stat)
            await callback.message.edit_text(text=text, reply_markup=cancel_kb())
        else:
            logger.error('Данные по статистике на найдены')

    else:
        logger.error('Пользователь не найден')

    await callback.answer()


def statistics_handlers(dp: Dispatcher):
    dp.callback_query.register(driver_statistic, F.data == 'user_stat')
    dp.callback_query.register(detail_statistic,  F.data.startswith('stat_'))
