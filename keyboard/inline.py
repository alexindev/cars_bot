from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_kb() -> InlineKeyboardMarkup:
    """ Главное меню """
    keyboard = InlineKeyboardBuilder()
    # keyboard.button(text='🧭 Текущий заказ', callback_data='current_order')
    keyboard.button(text='📊 Статистика', callback_data='user_stat')
    keyboard.button(text='💯 Качество', callback_data='quality')
    keyboard.button(text='🔝 Таблица лидеров', callback_data='leaderboard')
    keyboard.button(text='⚙ Настройки', callback_data='settings')
    keyboard.adjust(2, 1, 1)
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
    keyboard.button(text='⏳ День', callback_data='stat_day')
    keyboard.button(text='📆 Месяц', callback_data='stat_mounth')
    keyboard.button(text='↩', callback_data='cancel')
    keyboard.adjust(2)
    return keyboard.as_markup()


def settings_kb() -> InlineKeyboardMarkup:
    """ Меню настроек """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='🔎 Текущее состояние', callback_data='current_state')
    # keyboard.button(text='👼 Детское кресло', callback_data='seat')
    keyboard.button(text='💸 Режим оплаты', callback_data='payment')
    keyboard.button(text='📦 Режим доставки', callback_data='delivery')
    keyboard.button(text='🛣 Межгород', callback_data='incity')
    keyboard.button(text='↩', callback_data='cancel')
    keyboard.adjust(1)
    return keyboard.as_markup()


def seat_settings_kb() -> InlineKeyboardMarkup:
    """ Клавиатура детского кресла """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='ℹ Информация', callback_data='seat_info')
    keyboard.button(text='🔧 Добавить', callback_data='seat_add')
    keyboard.button(text='🗑 Удалить', callback_data='seat_delete')
    keyboard.button(text='↩', callback_data='cancel')
    keyboard.adjust(1)
    return keyboard.as_markup()


def seats_kb(param: str) -> InlineKeyboardMarkup:
    """ Кнопки выбора категории """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='0⃣ категория: 0-9 месяцев', callback_data=f'seat__{param}_0')
    keyboard.button(text='1⃣ категория: От 9 месяцев до 3 лет', callback_data=f'seat__{param}_1')
    keyboard.button(text='2⃣ категория: От 3 до 7 лет', callback_data=f'seat__{param}_2')
    keyboard.button(text='3⃣ категория: От 7 до 12 лет', callback_data=f'seat__{param}_3')
    keyboard.button(text='↩', callback_data='cancel')
    keyboard.adjust(1)
    return keyboard.as_markup()


def payment_settings_kb() -> InlineKeyboardMarkup:
    """ Клавиатура режима оплаты """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='💵 Наличные', callback_data='cash_on')
    keyboard.button(text='💳 Безналичные', callback_data='cash_off')
    keyboard.button(text='↩', callback_data='cancel')
    keyboard.adjust(1)
    return keyboard.as_markup()


def delivery_settings_kb() -> InlineKeyboardMarkup:
    """ Клавиатура режима доставки """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='👍 Включить', callback_data='delivery_on')
    keyboard.button(text='👎 Выключить', callback_data='delivery_off')
    keyboard.button(text='↩', callback_data='cancel')
    keyboard.adjust(1)
    return keyboard.as_markup()


def incity_settings_kb() -> InlineKeyboardMarkup:
    """ Клавиатура режима Mежгород """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='👍 Включить', callback_data='incity_on')
    keyboard.button(text='👎 Выключить', callback_data='incity_off')
    keyboard.button(text='↩', callback_data='cancel')
    keyboard.adjust(1)
    return keyboard.as_markup()
