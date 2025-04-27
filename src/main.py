from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from dotenv import load_dotenv
import os

from logging_bot import *

### выгрузка токена и админа из .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN = os.getenv("ADMIN")


class TelegramBot:
    pass


### инициальзация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


### запуск бота
async def main():
    logger.info("Бот запущен")
    await dp.start_polling(bot)


try:
    if __name__ == "__main__":
        asyncio.run(main())
except Exception as e:
    print(e)
