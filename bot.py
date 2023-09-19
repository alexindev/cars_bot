from loader import dp, bot
from handlers.commands import commands_handlers
from handlers.admin import bot_stopped, bot_started


async def start_bot():
    """Запуск бота"""

    commands_handlers(dp)
    dp.startup.register(bot_started)
    dp.shutdown.register(bot_stopped)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


