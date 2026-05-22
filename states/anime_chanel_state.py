from aiogram.fsm.state import StatesGroup, State

class AnimeChanelState(StatesGroup):
    id = State()
    del_id = State()