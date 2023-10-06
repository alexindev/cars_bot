from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


register_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🚖 Стать водителем | курьером')
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
            KeyboardButton(text='↩ Назад')
        ]
    ], resize_keyboard=True
)

information_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ℹ Информация')
        ]
    ], resize_keyboard=True
)

select_career_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🚕 Водитель такси')
        ],
        [
            KeyboardButton(text='🚗 Автокурьер')
        ],
        [
            KeyboardButton(text='🚶 Пеший курьер')
        ],
        [
            KeyboardButton(text='↩ Назад')
        ]
    ], resize_keyboard=True
)

next_or_back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Далее ▶')
        ],
        [
            KeyboardButton(text='↩ Назад')
        ]
    ], resize_keyboard=True
)

cancel_reg_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='↩ Назад')
        ]
    ], resize_keyboard=True
)


def get_cities_kb(cities: list) -> ReplyKeyboardMarkup:
    keyboard = []
    for city in cities:
        keyboard.append([KeyboardButton(text=f'{city.get("name")}')])
    keyboard.append([KeyboardButton(text='↩ Назад')])
    select_cities = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
    return select_cities
