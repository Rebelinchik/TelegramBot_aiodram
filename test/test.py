from aiogram import Bot, types, Dispatcher
from asyncio import run
import logging
from aiogram.filters.command import Command 


logging.basicConfig(level=logging.INFO)
bot = Bot(token="7952081601:AAGQqEOL5z4omSeFbe28yme0m-2sN-T-Pg4")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("start")

async def main():
    await dp.start_polling(bot)

try:
    run(main())
except Exception as e:
    print(e)