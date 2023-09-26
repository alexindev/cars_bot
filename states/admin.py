from aiogram.fsm.state import StatesGroup, State


class AdminComands(StatesGroup):
    get_phone = State()
