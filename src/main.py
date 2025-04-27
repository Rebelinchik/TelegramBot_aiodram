import asyncio
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from dotenv import load_dotenv

# свои модули
from logging_bot import logger
from memory_bot import *
from keyboard_bot import keyboard


###ТОКЕН
load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    logger.error("TOKEN не найден в файле")
    exit(1)


###КЛАСС БОТА
class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.dp = Dispatcher()
        ###Клавиатура
        self.button = keyboard
        ###Регистрация всех хендлеров
        self.register_hundlers()

    def register_hundlers(self):
        self.dp.message.register(self.start, Command("start"))
        self.dp.message.register(self.other_text)

    ###Хендлеры
    # Старт
    async def start(self, message: types.Message):
        logger.info(f"Пользователь {message.from_user.id} запустил бота через /start")
        await message.answer(
            f"Здравствуй {message.from_user.username}.\nПожалуйста зарегистрируйся",
            reply_markup=self.button,
        )

    # Не обрабатываемые сообщения
    async def other_text(self, message: types.Message):
        logger.info(
            f"Пользователь {message.from_user.id} отправил необрабатываемое сообщение"
        )
        await message.answer(f"Я обрабатываю только команды с вcтроенной клавиатуры")
        if message.text:
            await message.answer(f"Твоё сообщение: {message.text}")

    ###Запуск бота
    async def run(self):
        logger.info("Бот запущен")
        await self.dp.start_polling(self.bot)


###точка входа
if __name__ == "__main__":
    try:
        bot = TelegramBot()
        asyncio.run(bot.run())
    except Exception as e:
        print(e)
