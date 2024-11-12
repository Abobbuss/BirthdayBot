from aiogram.fsm.state import State, StatesGroup


# Класс состояний
class Form(StatesGroup):
    start = State()
    name_registrate = State()
    name_create_present = State()
    message_to_present = State()
    wait_send = State()

