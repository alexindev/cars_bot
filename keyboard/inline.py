from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_kb() -> InlineKeyboardMarkup:
    """ Главное меню """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Статистика', callback_data='user_info')
    keyboard.button(text='Лидеры', callback_data='leaderboard')
    keyboard.button(text='Качество', callback_data='quality')
    keyboard.button(text='Настройки', callback_data='settings')
    keyboard.adjust(1)
    return keyboard.as_markup()


def settings_kb() -> InlineKeyboardMarkup:
    """ Меню настроек """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Детское кресло', callback_data='seat')
    keyboard.button(text='Режим оплаты', callback_data='payment')
    keyboard.button(text='Режим доставки', callback_data='delivery')
    keyboard.button(text='Отмена', callback_data='cancel')
    keyboard.adjust(1)
    return keyboard.as_markup()


def seat_settings() -> InlineKeyboardMarkup:
    """ Настройки десткого кресла """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Информация', callback_data='seat_info')
    keyboard.button(text='Добавить', callback_data='seat_add')
    keyboard.button(text='Удалить', callback_data='seat_delete')
    keyboard.button(text='Отмена', callback_data='cancel')
    keyboard.adjust(1)
    return keyboard.as_markup()


def payment_settings() -> InlineKeyboardMarkup:
    """ Настройки режима оплаты """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Наличные', callback_data='cash')
    keyboard.button(text='Безналичные', callback_data='noncash')
    keyboard.button(text='Отмена', callback_data='cancel')
    keyboard.adjust(1)
    return keyboard.as_markup()


def delivery_settings() -> InlineKeyboardMarkup:
    """ Настройки режима доставки """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Включить', callback_data='delivery_on')
    keyboard.button(text='Выключить', callback_data='delivery_off')
    keyboard.button(text='Включить', callback_data='cancel')
    keyboard.adjust(1)
    return keyboard.as_markup()
