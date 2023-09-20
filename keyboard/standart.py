from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


register_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📞 Отправить номер телефона', request_contact=True)
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)

