from loguru import logger
from datetime import date

logger.add(f'logs/{date.today()}.log',
           format='<white>{time:HH:mm:ss}</white>'
                  ' | <level>{level: <8}</level>'
                  ' | <white>{name}:{function}:{line}</white>'
                  ' | <white>{message}</white>',
           encoding='utf-8',
           level='INFO')
