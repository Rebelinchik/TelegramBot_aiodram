from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class MemoryBot(StatesGroup):
    waiting_link = State()

