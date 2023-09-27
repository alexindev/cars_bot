from loader import dp, bot
from handlers.admin import admin_handlers
from handlers.commands import commands_handlers
from handlers.users import user_handlers
from handlers.settings import settings_handlers
from handlers.statistics import statistics_handlers
from logs.config import logger


async def start_bot():
    """Запуск бота"""
    user_handlers(dp)
    commands_handlers(dp)
    settings_handlers(dp)
    statistics_handlers(dp)
    admin_handlers(dp)

    try:
        logger.info('Bot started')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
