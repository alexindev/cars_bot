from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_kb() -> InlineKeyboardMarkup:
    """ Главное меню """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='🧭 Текущий заказ', callback_data='current_order')
    keyboard.button(text='📊 Статистика', callback_data='user_stat')
    keyboard.button(text='💯 Качество', callback_data='quality')
    keyboard.button(text='⚙ Настройки', callback_data='settings')
    keyboard.button(text='🔝 Таблица лидеров', callback_data='leaderboard')
    keyboard.adjust(2, 2, 1)
    return keyboard.as_markup()


def back_kb() -> InlineKeyboardMarkup:
    """ Кнопка назад """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='↩', callback_data='back')
    return keyboard.as_markup()


def cancel_kb() -> InlineKeyboardMarkup:
    """ Кнопка отмены """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='↩', callback_data='cancel')
    return keyboard.as_markup()


def statistic_kb() -> InlineKeyboardMarkup:
    """ Клавиатура статистики водителя"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='День', callback_data='stat_day')
    keyboard.button(text='Месяц', callback_data='stat_mounth')
    keyboard.button(text='↩', callback_data='cancel')
    keyboard.adjust(2)
    return keyboard.as_markup()


def settings_kb() -> InlineKeyboardMarkup:
    """ Меню настроек """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='👼 Детское кресло', callback_data='seat')
    keyboard.button(text='💸 Режим оплаты', callback_data='payment')
    keyboard.button(text='📦 Режим доставки', callback_data='delivery')
    keyboard.button(text='↩', callback_data='cancel')
    keyboard.adjust(1)
    return keyboard.as_markup()


def seat_settings_kb() -> InlineKeyboardMarkup:
    """ Клавиатура детского кресла """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Информация', callback_data='seat_info')
    keyboard.button(text='Добавить', callback_data='seat_add')
    keyboard.button(text='Удалить', callback_data='seat_delete')
    keyboard.button(text='↩', callback_data='cancel')
    keyboard.adjust(1)
    return keyboard.as_markup()


def payment_settings_kb() -> InlineKeyboardMarkup:
    """ Клавиатура режима оплаты """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Наличные', callback_data='cash')
    keyboard.button(text='Безналичные', callback_data='noncash')
    keyboard.button(text='↩', callback_data='cancel')
    keyboard.adjust(1)
    return keyboard.as_markup()


def delivery_settings_kb() -> InlineKeyboardMarkup:
    """ Клавиатура режима доставки """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Включить', callback_data='delivery_on')
    keyboard.button(text='Выключить', callback_data='delivery_off')
    keyboard.button(text='↩', callback_data='cancel')
    keyboard.adjust(1)
    return keyboard.as_markup()
