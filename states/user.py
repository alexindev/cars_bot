from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    start_quiz = State()
    get_career = State()
    get_city = State()
    get_phone = State()
    next_step = State()
    get_name = State()
    get_car_info = State()
    get_doc_info = State()
    get_license = State()
    get_driver_info = State()
    final_step = State()
