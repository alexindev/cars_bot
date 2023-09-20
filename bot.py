from loader import dp, bot
from handlers.commands import commands_handlers
from handlers.users import user_hanlers
from keyboard.commands import set_commands
from logs.config import logger


async def start_bot():
    """Запуск бота"""
    # dp.startup.register(bot_started)
    # dp.shutdown.register(bot_stopped)

    await set_commands()
    user_hanlers(dp)
    commands_handlers(dp)
    try:
        logger.info('Bot started')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
