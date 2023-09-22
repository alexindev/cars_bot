from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from db.database import Database
from utils.data import Data

import os

load_dotenv()
storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')
dp = Dispatcher(storage=storage)
base = Database()
data = Data()
