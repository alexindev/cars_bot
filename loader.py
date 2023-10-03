from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from db.database import Database
from utils.api_data import Data

import os

from utils.park_data import parks

load_dotenv()
storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')
dp = Dispatcher(storage=storage)
base = Database()
data = Data()


for i in parks:
    api_key = i.get('api_key')
    client = i.get('client')
    park_id = i.get('park_id')
    session_id = i.get('session_id')
    name = i.get('name')
    base.new_park(api_key=api_key, client=client, park_id=park_id, session_id=session_id, name=name)
