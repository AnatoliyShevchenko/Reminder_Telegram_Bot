# Aiogram
from aiogram.fsm.state import State, StatesGroup


class StartBotStates(StatesGroup):
    choose_language = State()
    wait_timezone = State()
    request_for_confirm = State()

