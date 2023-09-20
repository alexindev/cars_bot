from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_kb() -> InlineKeyboardMarkup:
    """ Главное меню """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Аккаунт', callback_data='account')
    keyboard.button(text='Лидеры', callback_data='leaderboard')
    keyboard.button(text='Качество', callback_data='quality')
    keyboard.button(text='Настройки', callback_data='settings')
    keyboard.adjust(1)
    return keyboard.as_markup()
