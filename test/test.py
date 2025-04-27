from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from dotenv import load_dotenv
import os
import logging

### выгрузка токена и админа из .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN = os.getenv("ADMIN")


### проверка что токен найден
if not TOKEN:
    exit(1)


### логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


### инициальзация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


### состояние памати
class RegiterStates(StatesGroup):
    waiting_for_name = State()


### клавиатура регистрации
registration_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Регистрация")]], resize_keyboard=True
)


### хандлер команды старт
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} запустил бота")
    await message.answer("привет, зарегистрируйся", reply_markup=registration_kb)


### обработчик регистрации
@dp.message(F.text == "Регистрация")
async def register(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} начал регистрацию")
    await message.answer("Как тебя зовут?")
    await state.set_state(RegiterStates.waiting_for_name)


### обработчик получения имени
@dp.message(RegiterStates.waiting_for_name)
async def get_name(message: types.Message, state: FSMContext):
    user_name = message.text
    logger.info(f"Пользовател {message.from_user.id} зарегистрирован как {user_name}")
    await message.answer(f"Приятно познакомится, {user_name}")
    await state.clear()


### запуск бота
async def main():
    logger.info("Бот запущен")
    await dp.start_polling(bot)


try:
    if __name__ == "__main__":
        asyncio.run(main())
except Exception as e:
    print(e)
