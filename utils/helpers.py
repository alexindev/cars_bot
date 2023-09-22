from datetime import timedelta


def get_leaderboard_text(liders: list) -> str:
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


def get_statistic_text(statistic: dict) -> str:
    orders = statistic['orders'].get('count_completed')
    price = round(statistic['orders'].get('price'), 1)
    km = statistic['orders'].get('mileage')
    if km != 0:
        km = round(km / 1000, 1)

    cash = round(statistic['balances'].get('cash_collected'), 1)
    card = round(statistic['balances'].get('platform_card'), 1)
    corp_pay = round(statistic['balances'].get('platform_corporate'), 1)
    tips = round(statistic['balances'].get('platform_tip'), 1)
    promo = round(statistic['balances'].get('platform_promotion'), 1)
    bonus = round(statistic['balances'].get('platform_bonus'), 1)
    ya_fees = round(statistic['balances'].get('platform_fees'), 1)
    park_fees = round(statistic['balances'].get('partner_fees'), 1)
    total = round(statistic['balances'].get('total'), 1)

    work_time = timedelta(seconds=statistic['work_time'].get('seconds'))
    average_pay = round(statistic['work_time'].get('mph'), 1)

    text = (f'✅ Выполненных заказов: {orders}\n'
            f'⏲ Сумма с таксометра: {price}\n'
            f'📍 Пробег: {km}\n\n'
            f'💸 Наличными: {cash}\n'
            f'💳 Оплата по карте: {card}\n'
            f'💼 Корпоративная оплата: {corp_pay}\n'
            f'🤑 Чаевые: {tips}\n'
            f'💎 Промоакции: {promo}\n'
            f'🎁 Бонус: {bonus}\n'
            f'🔻 Комиссия платформы: {ya_fees}\n'
            f'🔻 Комиссия парка: {park_fees}\n'
            f'💰 ИТОГО: {total}\n\n'
            f'⌚ Часы работы: {work_time}\n'
            f'💸 Среднечасовой заработок: {average_pay}')
    return text
