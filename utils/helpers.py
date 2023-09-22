

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
