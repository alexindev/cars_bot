import os

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboard.standart import get_cities_kb, select_career_kb, send_phone_kb, register_kb, next_or_back, cancel_reg_kb
from loader import bot, base, data
from states.user import User
from utils.helpers import registry_preparation_text
from utils.text_answer import start_command_text


async def register_user(message: types.Message, state: FSMContext):
    """ Регистрация пользователей. Выбор профессии """
    await bot.send_message(message.from_user.id, text='Выберите кем вы хотите стать:', reply_markup=select_career_kb)
    await state.set_state(User.start_quiz)


async def select_city(message: types.Message, state: FSMContext):
    """ Выбрать город """
    cities = base.get_parks()
    await state.update_data(career=message.text, user=message.from_user.id)
    await bot.send_message(message.from_user.id, 'Выберите город:', reply_markup=get_cities_kb(cities))
    await state.set_state(User.get_city)


async def get_phone(message: types.Message, state: FSMContext):
    """ Получить номер телефона """
    await state.update_data(city=message.text)
    await bot.send_message(message.from_user.id, 'Для отправки номера телефона нажмине на "Отправить номер телефона"',
                           reply_markup=send_phone_kb)
    await state.set_state(User.get_phone)


async def process_register(message: types.Message, state: FSMContext):
    """ Получение номера телефона """
    phone = message.contact.phone_number
    if not phone.startswith('+'):
        phone = '+' + phone
    user_data = await state.get_data()
    await state.update_data(phone=phone)
    await bot.send_message(message.from_user.id, 'Проверка номера телефона может занять несколько минут...',
                           reply_markup=ReplyKeyboardRemove())
    park_data = base.get_parks()
    for park in park_data:
        park_id = park.get('park_id')
        client = park.get('client')
        api_key = park.get('api_key')
        driver = await data.get_driver_list(phone=phone, api_key=api_key, park_id=park_id, client=client)
        if driver:
            await bot.send_message(message.from_user.id,
                                   f'Данный номер уже зарегистрирован в городе {park.get("name")}.\n'
                                   f'Авторизуйтесь в главном меню 👉🏻 /start',
                                   reply_markup=cancel_reg_kb
                                   )
            await state.clear()
            return
    else:
        await bot.send_message(chat_id=os.getenv('CHANEL_ID'),
                               text=(f'⏳ Началась регистрация пользователя @{message.from_user.username}\n\n'
                                     f'Номер телефона: {phone}\n'
                                     f'Должность: {user_data.get("career")}\n'
                                     f'Город: {user_data.get("city")}\n')
                               )
        text = registry_preparation_text(await state.get_data())
        await bot.send_message(message.from_user.id, text, reply_markup=next_or_back)
        await state.set_state(User.next_step)


async def get_name(message: types.Message, state: FSMContext):
    """ Начало заполнние формы. Получить ФИО"""
    await bot.send_message(message.from_user.id, text='Введите ваше ФИО.\nПример: Волков Олег Евгеньевич',
                           reply_markup=cancel_reg_kb)
    await state.set_state(User.get_car_info)


async def get_car_info_and_reg_courier(message: types.Message, state: FSMContext):
    """ Получить информацию о машине и/или зарегистрировать курьера """
    user_answer = message.text.split(' ')
    if len(user_answer) == 3:
        user_data = await state.get_data()
        if user_data.get('career') == '🚶 Пеший курьер':
            phone = user_data.get('phone')
            career = user_data.get('career')
            city = user_data.get('city')

            text = (f'✅ Успешная регистрация!\n\n'
                    f'Должность: {career}\n'
                    f'Полное имя: {message.text}\n'
                    f'Телефон: {phone}\n'
                    f'Город: {city}\n')
            if message.from_user.username:
                text += f'Профиль: @{message.from_user.username}'

            await bot.send_message(chat_id=os.getenv('CHANEL_ID'), text=text)

            await bot.send_message(message.from_user.id,
                                   text='✅ Данные приняты\n\n⏳ Ожидайте...\n👩‍💻 Мы уже начали проверку...',
                                   reply_markup=cancel_reg_kb)
            await state.clear()
            return

        await state.update_data(name=message.text)
        await bot.send_message(message.from_user.id,
                               text='Введите информацию об автомобиле:\n'
                                    'Гос номер\n'
                                    'Марка\n'
                                    'Модель\n'
                                    'Год выпуска\n'
                                    'Цвет\n\n'
                                    '<i>Пример: E023EE123, Ford, Mustang, 2020, Желтый</i>',
                               reply_markup=cancel_reg_kb)
        await state.set_state(User.get_doc_info)
    else:
        await bot.send_message(message.from_user.id,
                               'Не корректный формат ФИО, попробуйте еще раз\n Пример: Волков Олег Евгеньевич',
                               reply_markup=cancel_reg_kb)


async def get_doc_info(message: types.Message, state: FSMContext):
    """ Получить информацию о документах """
    if message.content_type == 'text':
        await state.update_data(car_info=message.text)
        await bot.send_message(message.from_user.id,
                               text='Введите информацию свидетельства о регистрации (серию и номер)\n\n'
                                    '<i>Пример: 99УВ188410</i>',
                               reply_markup=cancel_reg_kb)
        await state.set_state(User.get_license)
    else:
        await bot.send_message(message.from_user.id,
                               'Не корректный тип данных введите информацию об автомобиле',
                               reply_markup=cancel_reg_kb)


async def get_license(message: types.Message, state: FSMContext):
    """ Получить информацию о водительском удостоверении """
    if message.content_type == 'text':
        await state.update_data(sts=message.text)
        await bot.send_message(message.from_user.id,
                               text='Введите информацию о водительском удостоверении (серию и номер)\n\n'
                                    '<i>Пример: 3130635571</i>',
                               reply_markup=cancel_reg_kb)
        await state.set_state(User.get_driver_info)
    else:
        await bot.send_message(message.from_user.id,
                               'Не корректный тип данных введите информацию свидетельсва о регистрации',
                               reply_markup=cancel_reg_kb)


async def get_driver_info(message: types.Message, state: FSMContext):
    """ Получить информацию о стаже водителя """
    if message.content_type == 'text':
        await state.update_data(license=message.text)
        await bot.send_message(message.from_user.id,
                               text='Введите информацию о дате выдачи, дате окончании водительского удостоерения и о '
                                    'сроке водительского стажа)\n\n'
                                    '<i>Пример: дата выдачи: 15.06.2015, дата окончания: 16.06.2025, стаж 8 лет</i>',
                               reply_markup=cancel_reg_kb)
        await state.set_state(User.final_step)
    else:
        await bot.send_message(message.from_user.id,
                               'Не корректный тип данных введите информацию о водительском удостоверении',
                               reply_markup=cancel_reg_kb)


async def register_driver(message: types.Message, state: FSMContext):
    """ Регистрация водителя """
    if message.content_type == 'text':
        user_data = await state.get_data()
        name = user_data.get('name')
        phone = user_data.get('phone')
        career = user_data.get('career')
        city = user_data.get('city')

        text = (f'✅ Успешная регистрация!\n\n'
                f'Должность: {career}\n'
                f'Полное имя: {name}\n'
                f'Телефон: {phone}\n'
                f'Город: {city}\n'
                f'Данные об авто: {user_data.get("car_info")}\n'
                f'Свидетельство о регистрации: {user_data.get("sts")}\n'
                f'Водительское удостоверение: {user_data.get("license")}\n'
                f'Информация о стаже: {message.text}')
        if message.from_user.username:
            text += f'Профиль: @{message.from_user.username}'

        await bot.send_message(chat_id=os.getenv('CHANEL_ID'),
                               text=text)
        await bot.send_message(message.from_user.id,
                               text='✅ Данные приняты\n\n⏳ Ожидайте...\n👩‍💻 Мы уже начали проверку...',
                               reply_markup=cancel_reg_kb)
        await state.clear()
    else:
        await bot.send_message(message.from_user.id,
                               'Не корректный тип данных введите информацию о водительском стаже',
                               reply_markup=cancel_reg_kb)


async def start_menu(message: types.Message, state: FSMContext):
    """ Стартовое сообщение """
    await state.clear()
    await bot.send_message(message.from_user.id, text=start_command_text, reply_markup=register_kb)


def regisres_handlers(dp: Dispatcher):
    dp.message.register(start_menu, (F.text == '↩ Назад') | (F.text == '/start'))
    dp.message.register(register_user, (F.text == '🚖 Стать водителем | курьером'))
    dp.message.register(select_city, User.start_quiz,
                        (F.text == '🚕 Водитель такси') | (F.text == '🚗 Автокурьер') | (F.text == '🚶 Пеший курьер'), )
    dp.message.register(get_phone, User.get_city)
    dp.message.register(process_register, User.get_phone)
    dp.message.register(get_name, User.next_step)
    dp.message.register(get_car_info_and_reg_courier, User.get_car_info)
    dp.message.register(get_doc_info, User.get_doc_info)
    dp.message.register(get_license, User.get_license)
    dp.message.register(get_driver_info, User.get_driver_info)
    dp.message.register(register_driver, User.final_step)
