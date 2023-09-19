from loader import bot

import os


async def bot_started():
    await bot.send_message(os.getenv('ADMIN'), text='Бот запущен')


async def bot_stopped():
    await bot.send_message(os.getenv('ADMIN'), text='Бот остановлен')

