from aiogram import types, Dispatcher, F

from keyboard.inline import statistic_kb


async def driver_statistic(callback: types.CallbackQuery):
    """ Меню статистики """
    await callback.message.edit_text('Выберите пункт: 👇', reply_markup=statistic_kb())
    await callback.answer()


def statistics_handlers(dp: Dispatcher):
    dp.callback_query.register(driver_statistic, F.data == 'user_stat')

