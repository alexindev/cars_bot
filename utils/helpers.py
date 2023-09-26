from datetime import timedelta, datetime


def get_leaderboard_text(liders: list) -> str:
    """ Текст для отображения таблицы лидеров """
    text = ''
    for i, lider in enumerate(liders[:3], start=1):
        fullname, orders = lider.split()[:2], lider.split()[-1]
        medal = '🥇' if i == 1 else '🥈' if i == 2 else '🥉'
        text += f'{medal} {" ".join(fullname)} - {orders} заказов\n'

    if len(liders) >= 4:
        for lider in liders[3:]:
            fullname, orders = lider.split()[:2], lider.split()[-1]
            text += f'🎗 {" ".join(fullname)} - {orders} заказов\n'
    return text


def get_statistic_text(stat: dict, cancelled: list) -> str:
    """ Текст ответа для отображения статистики """
    orders = stat['orders'].get('count_completed')
    price = round(stat['orders'].get('price'), 1)
    km = stat['orders'].get('mileage')
    if km != 0:
        km = round(km / 1000, 1)

    cash = round(stat['balances'].get('cash_collected'), 1)
    card = round(stat['balances'].get('platform_card'), 1)
    corp_pay = round(stat['balances'].get('platform_corporate'), 1)
    tips = round(stat['balances'].get('platform_tip'), 1)
    promo = round(stat['balances'].get('platform_promotion'), 1)
    bonus = round(stat['balances'].get('platform_bonus'), 1)
    ya_fees = round(stat['balances'].get('platform_fees'), 1)
    park_fees = round(stat['balances'].get('partner_fees'), 1)
    total = round(stat['balances'].get('total'), 1)

    work_time = timedelta(seconds=stat['work_time'].get('seconds'))
    average_pay = round(stat['work_time'].get('mph'), 1)

    text = (f'✅ Выполненных заказов: {orders}\n'
            f'🧾 Сумма с таксометра: {price}\n'
            f'📍 Пробег: {km}\n\n'
            f'💸 Наличными: {cash}\n'
            f'💳 Оплата по карте: {card}\n'
            f'💼 Корпоративная оплата: {corp_pay}\n'
            f'🤑 Чаевые: {tips}\n'
            f'💎 Промоакции: {promo}\n'
            f'🎁 Бонус: {bonus}\n\n'
            f'🙅 Заказ отменен клиентом: {cancelled.count("Заказ отменён клиентом")}\n'
            f'🙅‍♂ Водитель отказался от заказа: {cancelled.count("Водитель отказался от заказа")}\n'
            f'✈ Самолет: {cancelled.count("Не смогли назначить заказ на водителя")}\n\n'
            f'🔻 Комиссия платформы: {ya_fees}\n'
            f'🔻 Комиссия парка: {park_fees}\n'
            f'💰 ИТОГО: {total}\n\n'
            f'⌚ Часы работы: {work_time}\n'
            f'💸 Среднечасовой заработок: {average_pay}')
    return text


def get_last_monday_sunday() -> tuple:
    """ Получить даты прыдыдуших понедельник и воскресенье """
    today = datetime.today()
    last_monday = today - timedelta(days=today.weekday(), weeks=1)
    last_sunday = last_monday + timedelta(days=6)

    monday_2 = today - timedelta(days=today.weekday(), weeks=2)
    sunday_2 = monday_2 + timedelta(days=6)

    last_monday = last_monday.strftime('%Y-%m-%d')
    last_sunday = last_sunday.strftime('%Y-%m-%d')

    monday_2 = monday_2.strftime('%Y-%m-%d')
    sunday_2 = sunday_2.strftime('%Y-%m-%d')
    return last_monday, last_sunday, monday_2, sunday_2


def get_quality_text(data: dict) -> str:
    """ Текст для отображения качества """
    our_observation = data.get("our_observation")
    our_observation_text = ', '.join(our_observation) if our_observation else '-'

    main_contains = data.get("main_complaints")
    main_contains_str = ', '.join(main_contains) if main_contains else '-'

    date_from = data.get('date_from').split('-')
    date_to = data.get('date_to').split('-')

    text = (f'📅 Показатели качества за период {date_from[2]}/{date_from[1]} - {date_to[2]}/{date_to[1]}: \n\n'
            f'👋 Предложено поездок: {data.get("orders")}\n'
            f'✌ Выполнено поездок: {data.get("trips")}\n'
            f'⭐ Заказы с оценкой 5 звезд: {data.get("perfect_trips")}\n'
            f'🤬 Жалобы на отмены поездок: {data.get("cancel_orders")}\n'
            f'❗ Нарушения стандартов сервиса: {our_observation_text}\n'
            f'‼ Основные жалобы пассажиров: {main_contains_str}\n'
            f'💔 Заказы с оценкой 1-3 звезды: {data.get("bad_rated_trips")}\n'
            f'🚩 Рейтинг в начале периода: {data.get("rating_start")}\n'
            f'🏁 Рейтинг в конце периода: {data.get("rating_end")}')
    return text


def get_state_text(data: dict) -> str:
    """ Текст для отображения текущего состояния """
    categories = {
        'econom': 'Эконом',
        'courier': 'Курьер',
        'intercity': 'Межгород',
        'express': 'Доставка',
        'comfort': 'Комфорт',
        'comfort_plus': 'Комфорт+',
        'vip': 'VIP',
        'business': 'Бизнес',
        'ultimate': 'Premier',
        'personal_driver': 'Персональный водитель',
        'maybach': 'Elite',
        'premium_suv': 'Помощь взрослым'
    }
    categories_text = ', '.join([categories.get(i, '-') for i in data.get('categories', [])])

    amenities = {
        'child_seat': 'Детское кресло',
        'lightbox': 'LightBox',
        'sticker': 'Наклейки',
        'delivery': 'Доставка'
    }
    amenities_text = ', '.join([amenities.get(i, '-') for i in data.get('amenities', [])])
    text = ('ℹ Текущее состояние: \n\n'
            f'🚘 Автомобиль: {data.get("brand")} {data.get("model")} {data.get("color")} {data.get("number")}\n'
            f'📅 Дата выпуска: {data.get("year")}\n'
            f'🔰 VIN: {data.get("vin")}\n'
            f'➕ Подключенные услуги: {amenities_text}\n'
            f'🔧 Тарифы: {categories_text}')
    return text


def get_seat_text(seats: list) -> str:
    """ Текст для информации о детских креслах """
    text = []
    for i in seats:
        if i[-1] == '0':
            text.append('0-9 месяцев')
        elif i[-1] == '1':
            text.append('От 9 месяцев до 3 лет')
        elif i[-1] == '2':
            text.append('От 3 до 7 лет')
        else:
            text.append('От 7 до 12 лет')
    return f'👀 Добавлены кресла категории: {", ".join(text)}'


def show_priority_drivers_text(data: tuple) -> str:
    """ Текст для вывода приоритетных водителей """
    text = '😎 Список приоритетных водителей: \n\n'
    for i in data:
        text += f'{i[0].full_name}: {i[0].phone}\n'
    return text
