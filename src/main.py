import asyncio
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv

# свои модули
from logging_bot import logger
from memory_bot import FSMContext, MemoryBot
from keyboard_bot import keyboard
from sql import *
from scripts import create_link_in_text

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
        self.dp.message.register(self.registration_on_db, F.text == "Регистрация")
        self.dp.message.register(self.link, F.text == "Добавить желание")
        self.dp.message.register(self.get_link, MemoryBot.waiting_link)
        self.dp.message.register(self.other_text)

    ###Хендлеры
    # Старт
    async def start(self, message: types.Message):
        logger.info(f"Пользователь {message.from_user.id} запустил бота через /start")
        await message.answer(
            f"Здравствуй {message.from_user.username}.\nПожалуйста зарегистрируйся",
            reply_markup=self.button,
        )

    # регистрация в базе данных
    async def registration_on_db(self, message: types.Message):
        try:
            if not ischeck_user_in_db(int(message.from_user.id)):
                add_user_db(int(message.from_user.id), str(message.from_user.username))
                logger.info(
                    f"Пользователь {message.from_user.id} зарегистрирован в базе данных"
                )
                await message.answer(
                    f"{message.from_user.username}, вы зарегистированны в базе данных"
                )
            else:
                await message.answer("Вы уже зарегистрированы")
        except Exception as e:
            logger.error(f"Произошла ошибка при регистрации в главном файле: {e}")

    # Запуск добавления ссылки в строку пользователя в базе данных
    async def link(self, message: types.Message, state: FSMContext):
        if ischeck_user_in_db(int(message.from_user.id)):
            logger.info(f"Пользователь {message.from_user.id} начал запись ссылки")
            await message.answer("Хорошо, поделись со мной желанием с маркетплейса")
            await state.set_state(MemoryBot.waiting_link)
        else:
            await message.answer("Для начала зарегистрируйся")

    # обработка добавления ссылки
    async def get_link(self, message: types.Message, state: FSMContext):
        if "http" in message.text:
            link = create_link_in_text(message.text)
            try:
                add_link_db(int(message.from_user.id), str(link))
                logger.info(f"Пользователь {message.from_user.id} сохранил свое желание")
                await message.answer(
                    f"Твоё желание сохранено, {message.from_user.username}"
                )
                await state.clear()
            except Exception as e:
                logger.error(
                    f"ошибка при сохранении ссылки пользователя {message.from_user.id} в основном коде: {e}"
                )
                await message.answer("Что то пошло не так, попробуйте позже")
        else:
            logger.error(f"Пользователь {message.from_user.id} не отправил ссылку, ссылка не сохранена")
            await message.reply("В этом сообщении нет ссылки на желание, твоё желание не сохранено")
            await state.clear()

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
