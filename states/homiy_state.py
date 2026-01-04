from aiogram.fsm.state import StatesGroup, State

class HomiyState(StatesGroup):
    id = State()
    link = State()
    del_id = State()