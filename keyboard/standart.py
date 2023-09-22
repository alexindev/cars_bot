from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


register_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🚖 Стать водитилем | курьером')
        ],
        [
            KeyboardButton(text='🔑 Авторизация')
        ],
        [
            KeyboardButton(text='ℹ Информация о парке')
        ]
    ], resize_keyboard=True
)


send_phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📞 Отправить номер телефона', request_contact=True)
        ],
        [
            KeyboardButton(text='↩ Отмена')
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)
