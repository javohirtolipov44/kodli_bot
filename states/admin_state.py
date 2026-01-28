from aiogram.fsm.state import StatesGroup, State

class AdminState(StatesGroup):

    admin_panel = State()
    send_message = State()
